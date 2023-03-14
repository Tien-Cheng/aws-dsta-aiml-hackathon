import { useState } from "react";
import {
    Box,
    IconButton,
    Typography,
    useTheme,
    useMediaQuery
} from "@mui/material";
import {
    DarkMode,
    LightMode,
    Menu,
    Close
} from "@mui/icons-material";
import { useDispatch } from "react-redux";
import { setMode } from "state";
import FlexBetween from "components/FlexBetween";

const Navbar = () => {
    const [isMobileMenuToggled, setIsMobileMenuToggled] = useState(false);
    const dispatch = useDispatch();
    const isNonMobileScreens = useMediaQuery("(min-width: 1000px)");

    const theme = useTheme();
    const dark = theme.palette.neutral.dark;
    const background = theme.palette.background.default;
    const alt = theme.palette.background.alt;

    return (
        <FlexBetween padding="1rem 6%" backgroundColor={alt}>
        <FlexBetween gap="1.75rem">
          <Typography
            fontWeight="bold"
            fontSize="clamp(1rem, 2rem, 2.25rem)"
            color="primary"
            sx={{
              "&:hover": {
                cursor: "default"
              }
            }}
          >
            BuYaoMafan
          </Typography>
        </FlexBetween>
  
        {/* DESKTOP NAV */}
        {isNonMobileScreens ? (
          <FlexBetween gap="2rem">
            <IconButton onClick={() => dispatch(setMode())}>
              {theme.palette.mode === "dark" ? (
                <DarkMode sx={{ fontSize: "25px" }} />
              ) : (
                <LightMode sx={{ color: dark, fontSize: "25px" }} />
              )}
            </IconButton>
          </FlexBetween>
        ) : (
          <IconButton onClick={() => setIsMobileMenuToggled(!isMobileMenuToggled)}>
            <Menu />
          </IconButton>
        )}
  
        {/* MOBILE NAV */}
        {!isNonMobileScreens && isMobileMenuToggled && (
          <Box
            position="fixed"
            right="0"
            bottom="0"
            height="100%"
            zIndex="10"
            maxWidth="500px"
            minWidth="300px"
            backgroundColor={background}
          >
            {/* CLOSE ICON */}
            <Box display="flex" justifyContent="flex-end" p="1rem">
              <IconButton onClick={() => setIsMobileMenuToggled(!isMobileMenuToggled)}>
                <Close />
              </IconButton>
            </Box>
  
            {/* MENU ITEMS */}
            <FlexBetween
              display="flex"
              flexDirection="column"
              justifyContent="center"
              alignItems="center"
              gap="3rem"
            >
              <IconButton onClick={() => dispatch(setMode())} sx={{ fontSize: "25px" }}>
                {theme.palette.mode === "dark" ? (
                  <DarkMode sx={{ fontSize: "25px" }} />
                ) : (
                  <LightMode sx={{ color: dark, fontSize: "25px" }} />
                )}
              </IconButton>
            </FlexBetween>
          </Box>
        )}
      </FlexBetween>
    )
}

export default Navbar;