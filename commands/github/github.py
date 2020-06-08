#!/usr/bin/env python3

from subprocess import Popen, PIPE
import subprocess
import json, base64
import urllib.request, urllib.error, urllib.parse, argparse
import sys, os, tempfile


def jsonsearch(jsonObj, query):
    objs = [jsonObj]
    for o in query.split("."):
        new_objs = []
        for obj in objs:
            if type(obj) == dict:
                for k, v in list(obj.items()):
                    if o == "" or k == o:
                        new_objs.append(v)
            if type(obj) == list:
                if o == "":
                    new_objs.extend(obj)
        objs = new_objs

    return objs


class RequestWithMethod(urllib.request.Request):
    def __init__(self, *args, **kwargs):
        self._method = kwargs.pop("method", None)
        urllib.request.Request.__init__(self, *args, **kwargs)

    def get_method(self):
        return (
            self._method
            if self._method
            else super(RequestWithMethod, self).get_method()
        )


class GitHub:
    """The GitHub Class"""

    def __init__(self, username, token):
        self.username = username
        self.token = token

        self.api_version = "v3"
        self.api_base_url = "https://api.github.com"
        self.debug = False
        self.return_false_on_error = True

    class error(Exception):
        def __init__(self, message, code=0, request=False):
            self.message = message
            self.code = code
            self.request = request

        def __str__(self):
            return "GitHub Error: {0} ({1})".format(self.message, self.code)

    def _throw(self, error):
        if self.debug:
            print((str(error)))

        if self.return_false_on_error:
            return False

        raise error

    @staticmethod
    def get_authentication_from_config():
        (username, stderr) = Popen(
            ["git", "config", "github.user"], stdout=PIPE, text=True
        ).communicate()
        (token, stderr) = Popen(
            ["git", "config", "github.token"], stdout=PIPE, text=True
        ).communicate()
        if username and token:
            return (username.strip(), token.strip())
        return None

    @staticmethod
    def setup_config():
        print("Github Tool Setup")
        username = prompt("Github username:")
        if not username:
            print("Please provide a github username")
            return
        token = prompt("Github API token:")
        if not token:
            print("Please provide an API token")
            return

        Popen(["git", "config", "--global", "github.user", username], text=True)
        Popen(["git", "config", "--global", "github.token", token], text=True)

        print("Config saved")
        return True

    @staticmethod
    def get_project(names=[]):
        if not names:
            (project, stderr) = Popen(
                ["git", "remote", "get-url", "origin"],
                stdout=PIPE,
                stderr=PIPE,
                text=True,
            ).communicate()
            if not project:
                (project, stderr) = Popen(
                    ["git", "remote", "get-url", "gh"],
                    stdout=PIPE,
                    stderr=PIPE,
                    text=True,
                ).communicate()
        else:
            for name in names:
                (project, stderr) = Popen(
                    ["git", "remote", "get-url", name],
                    stdout=PIPE,
                    stderr=PIPE,
                    text=True,
                ).communicate()
                if project:
                    break

        project = project.strip()
        if not "github" in project:
            project = None
        else:
            project = project.replace("git@github.com:", "")
            project = project.replace(".git", "")

        return project

    def _request(self, rest, params=None, method="GET", page=False):
        if self.api_base_url not in rest:
            request_url = self.api_base_url + "/" + rest
        else:
            request_url = rest

        if self.debug:
            print(request_url)
            print(params)

        response = False
        try:
            base64string = (
                base64.encodestring(f"{self.username}:{self.token}".encode())
                .decode("ascii")
                .replace("\n", "")
            )
            headers = {"Authorization": "Basic %s" % base64string}
            req = RequestWithMethod(request_url, headers=headers, method=method)
            if params:
                post_body = json.dumps(params).encode()
                req = RequestWithMethod(
                    request_url, post_body, headers=headers, method=method
                )

            handler = urllib.request.urlopen(req)
            links = handler.info().getallmatchingheaders("Link")
            response = handler.read()
        except IOError as error:
            if self.debug:
                print((error.read()))
                print(("Error Making Request: " + str(error)))
            return self._throw(error)

        if response:
            response_object = json.loads(response)
            if self.debug:
                print(response_object)

            if page and links:
                link = {}
                for l in links.split(", "):
                    first, last = l.split("; ")
                    name = last.replace('rel="', "")[:-1]
                    value = first[1:-1]
                    link[name] = value
                if "next" in link and "last" in link:
                    second_response = self._request(
                        link["next"], method=method, page=link["next"] != link["last"]
                    )
                try:
                    response_object += second_response
                except:
                    pass
            return response_object
        return True

    def repo_list(self):
        repos = self._request("user/repos", page=True)
        return repos

    def repo_create(self, repo, private, description="", org=None):
        url = "user/repos"
        if org is not None:
            url = "orgs/" + org + "/repos"
        created = self._request(
            url,
            method="POST",
            params={"name": repo, "private": private, "description": description},
        )
        return created

    def repo_edit(self, repo, private=None, description=None):
        params = {}
        if private != None:
            params["private"] = private
        if description != None:
            params["description"] = description

        params["name"] = repo.split("/")[-1]

        edited = self._request("repos/" + repo, method="PATCH", params=params)
        return edited

    def repo_delete(self, repo):
        deleted = self._request("repos/" + repo, method="DELETE")
        return deleted

    def repo_collab_list(self, repo):
        collabs = self._request("repos/" + repo + "/collaborators", page=True)
        return collabs

    def repo_collab(self, repo, collab, remove=False):
        method = "PUT"
        if remove:
            method = "DELETE"
        collab = self._request(
            "repos/" + repo + "/collaborators/" + collab, method=method
        )
        return collab

    def key_list(self):
        keys = self._request("user/keys", page=True)
        return keys

    def key_create(self, title, key):
        created = self._request(
            "user/keys",
            params={"title": title, "key": key, "wiki": False},
            method="POST",
        )
        return created

    def key_delete(self, key_id):
        deleted = self._request("user/keys/" + key_id, method="DELETE")
        return deleted

    def fork(self, repo):
        fork = self._request("repos/" + repo + "/forks", method="POST")
        return fork

    def pull_request(self, repo_name, title, head, base, body):
        p = {"title": title, "head": head, "base": base, "body": body}
        request = self._request(
            "repos/" + repo_name + "/pulls", params=p, method="POST"
        )
        return request

    def pulls_list(self, repo_name):
        pulls = self._request("repos/" + repo_name + "/pulls", method="GET", page=True)
        return pulls

    def pulls_get(self, repo_name, number):
        pulls = self._request(
            "repos/" + repo_name + "/pulls/" + str(number), method="GET"
        )
        return pulls

    def pull_info(self, repo_name, pull):
        info = self._request("repos/" + repo_name + "/pulls/" + pull, method="GET")
        return info

    def pull_comments(self, repo_name, pull):
        comments = self._request(
            "repos/" + repo_name + "/issues/" + pull + "/comments",
            method="GET",
            page=True,
        )
        return comments

    def issue_create(self, repo_name, title, body):
        p = {"title": title, "body": body}
        request = self._request(
            "repos/" + repo_name + "/issues", params=p, method="POST"
        )
        return request

    def issues_list(self, repo_name):
        issues = self._request(
            "repos/" + repo_name + "/issues", method="GET", page=True
        )
        return issues

    def issue_info(self, repo_name, issue):
        info = self._request("repos/" + repo_name + "/issues/" + issue, method="GET")
        return info

    def issue_comments(self, repo_name, issue):
        comments = self._request(
            "repos/" + repo_name + "/issues/" + issue + "/comments",
            method="GET",
            page=True,
        )
        return comments

    def issue_events(self, repo_name, issue):
        events = self._request(
            "repos/" + repo_name + "/issues/" + issue + "/events",
            method="GET",
            page=True,
        )
        return events

    def issue_comment(self, repo_name, issue, body):
        comment = self._request(
            "repos/" + repo_name + "/issues/" + issue + "/comments",
            {"body": body},
            "POST",
        )
        return comment

    def ref_status(self, repo_name, ref):
        status = self._request(
            "repos/" + repo_name + "/commits/" + ref + "/status",
            {"ref": ref},
            method="GET",
        )
        return status
