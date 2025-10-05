from typing import Optional, List

import attr
from datetime import datetime


@attr.s(auto_attribs=True)
class CommentData:
    """Data class to hold comment data information."""
    comment_id: str = attr.ib(validator=attr.validators.instance_of(str))
    post_id: str = attr.ib(validator=attr.validators.instance_of(str))
    score: int = attr.ib(default=0, validator=attr.validators.instance_of(int))
    body: Optional[str] = attr.ib(default=None, validator=attr.validators.optional(attr.validators.instance_of(str)))


@attr.s(auto_attribs=True)
class ScrapedData:
    """Data class to hold scraped data information."""
    post_id: str = attr.ib(validator=attr.validators.instance_of(str))
    id: Optional[int] = attr.ib(default=None, validator=attr.validators.optional(attr.validators.instance_of(int)))
    title: Optional[str] = attr.ib(default=None, validator=attr.validators.optional(attr.validators.instance_of(str)))
    score: int = attr.ib(default=0, validator=attr.validators.instance_of(int))
    comments: Optional[List[CommentData]] = attr.ib(default=None, validator=attr.validators.optional(
        attr.validators.deep_iterable(
            member_validator=attr.validators.instance_of(CommentData),
            iterable_validator=attr.validators.instance_of(list)
        )))
    collected_at: Optional[datetime] = attr.ib(default=None, validator=attr.validators.optional(
        attr.validators.instance_of(datetime)))
    processing_started_at: Optional[datetime] = attr.ib(default=None, validator=attr.validators.optional(
        attr.validators.instance_of(datetime)))
    processed_at: Optional[datetime] = attr.ib(default=None, validator=attr.validators.optional(
        attr.validators.instance_of(datetime)))
    status: str = attr.ib(default='collected', validator=attr.validators.instance_of(
        str))  # collected, ignored, processing, processed, failed
    error_message: Optional[str] = attr.ib(default=None,
                                           validator=attr.validators.optional(attr.validators.instance_of(str)))


@attr.s(auto_attribs=True)
class RedditData(ScrapedData):
    """Data class to hold Reddit data information."""
    subreddit: Optional[str] = attr.ib(default=None,
                                       validator=attr.validators.optional(attr.validators.instance_of(str)))
