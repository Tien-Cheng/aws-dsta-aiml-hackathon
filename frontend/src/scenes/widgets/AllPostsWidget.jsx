import { useSelector } from "react-redux";
import PostWidget from "./PostWidget";

const AllPostsWidget = () => {
  const posts = useSelector((state) => state.posts);

  return (
    <>
        {posts.length > 0 && posts.slice(0).reverse().map(
            ({
                // FIELDS DEPENDENT ON RETURN FROM AI/ML IN JSON FORMAT (backend)
            description,
            location
            }, index) => (
            <PostWidget
                description={description}
                location={location}
                key={index}
            />
            )
        )}
    </>
  );
};

export default AllPostsWidget;