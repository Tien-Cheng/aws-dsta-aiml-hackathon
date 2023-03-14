import { Box, useMediaQuery } from "@mui/material";
import Navbar from "scenes/nav";
import InputPostWidget from "scenes/widgets/InputPostWidget";
import AllPostsWidget from "scenes/widgets/AllPostsWidget";

const HomePage = () => {
    const isNonMobileScreens = useMediaQuery("(min-width:1000px)");

    return (
        <Box>
            <Navbar />
            <Box
                width="100%"
                padding="2rem 6%"
                display={isNonMobileScreens ? "flex" : "block"}
                gap="0.5rem"
                justifyContent="center"
            >
                <Box
                flexBasis={isNonMobileScreens ? "80%" : undefined}
                mt={isNonMobileScreens ? undefined : "2rem"}
                >
                <InputPostWidget />
                <AllPostsWidget />
                </Box>
            </Box>
        </Box>
    )
}

export default HomePage;