from typing import Optional

from specklepy.api.models import Branch
from specklepy.core.api.resources.branch import Resource as CoreResource
from specklepy.logging import metrics


class Resource(CoreResource):
    """API Access class for branches"""

    def __init__(self, account, basepath, client) -> None:
        super().__init__(
            account=account,
            basepath=basepath,
            client=client,
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
        metrics.track(metrics.SDK, self.account, {"name": "Branch Create"})
        return super().create(stream_id, name, description)

    def get(self, stream_id: str, name: str, commits_limit: int = 10):
        """Get a branch by name from a stream

        Arguments:
            stream_id {str} -- the id of the stream to get the branch from
            name {str} -- the name of the branch to get
            commits_limit {int} -- maximum number of commits to get

        Returns:
            Branch -- the fetched branch with its latest commits
        """
        metrics.track(metrics.SDK, self.account, {"name": "Branch Get"})
        return super().get(stream_id, name, commits_limit)

    def list(self, stream_id: str, branches_limit: int = 10, commits_limit: int = 10):
        """Get a list of branches from a given stream

        Arguments:
            stream_id {str} -- the id of the stream to get the branches from
            branches_limit {int} -- maximum number of branches to get
            commits_limit {int} -- maximum number of commits to get

        Returns:
            List[Branch] -- the branches on the stream
        """
        metrics.track(metrics.SDK, self.account, {"name": "Branch List"})
        return super().list(stream_id, branches_limit, commits_limit)

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
        metrics.track(metrics.SDK, self.account, {"name": "Branch Update"})
        return super().update(stream_id, branch_id, name, description)

    def delete(self, stream_id: str, branch_id: str):
        """Delete a branch

        Arguments:
            stream_id {str} -- the id of the stream containing the branch to delete
            branch_id {str} -- the branch to delete

        Returns:
            bool -- True if deletion is successful
        """
        metrics.track(metrics.SDK, self.account, {"name": "Branch Delete"})
        return super().delete(stream_id, branch_id)
