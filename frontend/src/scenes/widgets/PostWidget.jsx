import { Typography, useTheme } from "@mui/material";
import WidgetWrapper from "components/WidgetWrapper";

const PostWidget = ({description, location}) => {
    const { palette } = useTheme();
    const main = palette.neutral.main;

    return (
        <WidgetWrapper m="2rem 0">
            <Typography color={main}>
                {description}
            </Typography>
        </WidgetWrapper>
    );
};

export default PostWidget;