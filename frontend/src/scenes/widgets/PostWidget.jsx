import React from "react";
import { Typography, useTheme } from "@mui/material";
import WidgetWrapper from "components/WidgetWrapper";
import TableSummary from "components/TableSummary";

const PostWidget = ({description}) => {
    const { palette } = useTheme();
    const main = palette.neutral.main;
    
    const textDetails = description.posts?.toxicity_predictions;
    const contentDetails = description.posts?.content_warnings;

    return (
        <WidgetWrapper m="2rem 0">
            {contentDetails ? <Typography
                fontWeight="bold"
                fontSize="1rem"
                sx={{margin: "0.5rem 0"}}
                >
                Content Analysis</Typography> : <></>}
            {contentDetails && contentDetails.map((info, index) => {
                return (
                    <TableSummary key={index} header={info?.blob} rows={info?.classes} headerColor={main} image={true}/>
                )
            })}
            {textDetails ? <Typography
                fontWeight="bold"
                fontSize="1rem"
                sx={{margin: "0.5rem 0"}}
                >
                Text Analysis</Typography> : <></>}
            {textDetails && textDetails.map((cell, index) => {
                return (
                    <TableSummary key={index} header={cell?.text} rows={cell?.classes} headerColor={main} image={false}/>
                )
            })}
        </WidgetWrapper>
    );
};

export default PostWidget;