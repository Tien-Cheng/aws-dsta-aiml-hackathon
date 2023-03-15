import React from "react";
import { useTheme } from "@mui/material";
// import CustomPaginationActionsTable from "components/MultiTableSummary";
import WidgetWrapper from "components/WidgetWrapper";
import TableSummary from "components/TableSummary";
// import TextAnalysis from "components/TextAnalysis";
// import FlexBetween from "components/FlexBetween";

const PostWidget = ({description}) => {
    const { palette } = useTheme();
    const main = palette.neutral.main;
    
    const details = description.posts;

    return (
        <WidgetWrapper m="2rem 0">
            {details.map( (cell, index) => {
                return (
                    // <CustomPaginationActionsTable key={index} header={cell.text} rows={cell.classes} headerColor={main}/>
                    <TableSummary key={index} header={cell.text} rows={cell.classes} headerColor={main}/>
                    // <FlexBetween>
                    //     <TextAnalysis key={index} text={cell.text} note={cell.classes}/>
                    // </FlexBetween>
                )
                })
            }
        </WidgetWrapper>
    );
};

export default PostWidget;