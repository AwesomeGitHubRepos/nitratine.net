import React from "react";
import PostTile, { IPostTile } from "./PostTile";
import Pagination, { IPagination } from "./Pagination";

export interface IFeed {
  posts: IPostTile[];
  pagination: IPagination;
}

const Feed: React.FC<IFeed> = ({ posts, pagination }) => (
  <div>
    <h1 className="mb-4">Nitratine Blog Feed</h1>
    {posts.map(post => (
      <PostTile {...post} key={post.href} />
    ))}
    <Pagination {...pagination} />
  </div>
);

export default Feed;
