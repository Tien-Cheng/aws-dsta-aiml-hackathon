import { useSelector } from "react-redux";
import PostWidget from "./PostWidget";

const AllPostsWidget = () => {
  const posts = useSelector((state) => state.posts);

  return (
    <>
        {posts.length > 0 && posts.slice(0).reverse().map(
            (post, index) => (
            <PostWidget
                description={post}
                key={index}
            />
            )
        )}
    </>
  );
};

export default AllPostsWidget;