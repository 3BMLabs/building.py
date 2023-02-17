from typing import Optional

from gql import gql

from specklepy.api.models import Branch
from specklepy.api.resource import ResourceBase
from specklepy.logging import metrics

NAME = "branch"


class Resource(ResourceBase):
    """API Access class for branches"""

    def __init__(self, account, basepath, client) -> None:
        super().__init__(
            account=account,
            basepath=basepath,
            client=client,
            name=NAME,
        )
        self.schema = Branch

    def create(
        self, stream_id: str, name: str, description: str = "No description provided"
    ) -> str:
        """Create a new branch on this stream

        Arguments:
            name {str} -- the name of the new branch
            description {str} -- a short description of the branch

        Returns:
            id {str} -- the newly created branch's id
        """
        metrics.track(metrics.BRANCH, self.account, {"name": "create"})
        query = gql(
            """
            mutation BranchCreate($branch: BranchCreateInput!) {
              branchCreate(branch: $branch)
            }
          """
        )
        params = {
            "branch": {
                "streamId": stream_id,
                "name": name,
                "description": description,
            }
        }

        return self.make_request(
            query=query, params=params, return_type="branchCreate", parse_response=False
        )

    def get(self, stream_id: str, name: str, commits_limit: int = 10):
        """Get a branch by name from a stream

        Arguments:
            stream_id {str} -- the id of the stream to get the branch from
            name {str} -- the name of the branch to get
            commits_limit {int} -- maximum number of commits to get

        Returns:
            Branch -- the fetched branch with its latest commits
        """
        metrics.track(metrics.BRANCH, self.account, {"name": "get"})
        query = gql(
            """
            query BranchGet($stream_id: String!, $name: String!, $commits_limit: Int!) {
                stream(id: $stream_id) {
                        branch(name: $name) {
                          id,
                          name,
                          description,
                          commits (limit: $commits_limit) {
                            totalCount,
                            cursor,
                            items {
                              id,
                              referencedObject,
                              sourceApplication,
                              totalChildrenCount,
                              message,
                              authorName,
                              authorId,
                              branchName,
                              parents,
                              createdAt
                            }
                        }
                    }
                }
            }
            """
        )

        params = {"stream_id": stream_id, "name": name, "commits_limit": commits_limit}

        return self.make_request(
            query=query, params=params, return_type=["stream", "branch"]
        )

    def list(self, stream_id: str, branches_limit: int = 10, commits_limit: int = 10):
        """Get a list of branches from a given stream

        Arguments:
            stream_id {str} -- the id of the stream to get the branches from
            branches_limit {int} -- maximum number of branches to get
            commits_limit {int} -- maximum number of commits to get

        Returns:
            List[Branch] -- the branches on the stream
        """
        metrics.track(metrics.BRANCH, self.account, {"name": "get"})
        query = gql(
            """
            query BranchesGet(
                    $stream_id: String!,
                    $branches_limit: Int!,
                    $commits_limit: Int!
                ) {
                stream(id: $stream_id) {
                    branches(limit: $branches_limit) {
                        items {
                            id
                            name
                            description
                            commits(limit: $commits_limit) {
                                totalCount
                                items{
                                    id
                                    message
                                    referencedObject
                                    sourceApplication
                                    parents
                                    authorId
                                    authorName
                                    branchName
                                    createdAt
                                }
                            }
                        }
                    }
                }
            }
            """
        )

        params = {
            "stream_id": stream_id,
            "branches_limit": branches_limit,
            "commits_limit": commits_limit,
        }

        return self.make_request(
            query=query, params=params, return_type=["stream", "branches", "items"]
        )

    def update(
        self,
        stream_id: str,
        branch_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ):
        """Update a branch

        Arguments:
            stream_id {str} -- the id of the stream containing the branch to update
            branch_id {str} -- the id of the branch to update
            name {str} -- optional: the updated branch name
            description {str} -- optional: the updated branch description

        Returns:
            bool -- True if update is successful
        """
        metrics.track(metrics.BRANCH, self.account, {"name": "update"})
        query = gql(
            """
            mutation  BranchUpdate($branch: BranchUpdateInput!) {
                branchUpdate(branch: $branch)
                }
            """
        )
        params = {
            "branch": {
                "streamId": stream_id,
                "id": branch_id,
            }
        }

        if name:
            params["branch"]["name"] = name
        if description:
            params["branch"]["description"] = description

        return self.make_request(
            query=query, params=params, return_type="branchUpdate", parse_response=False
        )

    def delete(self, stream_id: str, branch_id: str):
        """Delete a branch

        Arguments:
            stream_id {str} -- the id of the stream containing the branch to delete
            branch_id {str} -- the branch to delete

        Returns:
            bool -- True if deletion is successful
        """
        metrics.track(metrics.BRANCH, self.account, {"name": "delete"})
        query = gql(
            """
            mutation BranchDelete($branch: BranchDeleteInput!) {
                branchDelete(branch: $branch)
            }
            """
        )

        params = {"branch": {"streamId": stream_id, "id": branch_id}}

        return self.make_request(
            query=query, params=params, return_type="branchDelete", parse_response=False
        )
