import {
    EditOutlined,
    DeleteOutlined,
    ImageOutlined,
    MicOutlined,
    MoreHorizOutlined,
    VideocamOutlined,
    NotesOutlined
} from "@mui/icons-material";
import {
    Box,
    Divider,
    Typography,
    InputBase,
    useTheme,
    Button,
    IconButton,
    useMediaQuery,
} from "@mui/material";
import FlexBetween from "components/FlexBetween";
import Dropzone from "react-dropzone";
import WidgetWrapper from "components/WidgetWrapper";
import { useState } from "react";
import { useDispatch } from "react-redux";
import { setPosts } from "state";
  
const InputPostWidget = () => {
    const dispatch = useDispatch();
    const [isText, setIsText] = useState(true);
    const [text, setText] = useState("");
    const [isImage, setIsImage] = useState(false);
    const [image, setImage] = useState(null);
    const [isVideo, setIsVideo] = useState(false);
    const [video, setVideo] = useState(null);
    const [isAudio, setIsAudio] = useState(false);
    const [audio, setAudio] = useState(null);
    const { palette } = useTheme();
    const isNonMobileScreens = useMediaQuery("(min-width: 1000px)");
    const mediumMain = palette.neutral.mediumMain;
    const medium = palette.neutral.medium;
  
    const handlePost = async () => {
        const formData = new FormData();
        if (isText) {
            formData.append("type", "text");
            formData.append("description", text);
        } else if (isImage) {
            formData.append("type", "image");
            formData.append("file", image);
            formData.append("filePath", image.name);
        } else if (isVideo) {
            formData.append("type", "video");
            formData.append("file", video);
            formData.append("filePath", video.name);
        } else if (isAudio) {
            formData.append("type", "audio");
            formData.append("file", audio);
            formData.append("filePath", audio.name);
        }

        const response = await fetch(`http://localhost:8888/posts`, {
            method: "POST",
            body: formData
        });
        const posts = await response.json();
        dispatch(setPosts({ posts }));
        setText("");
        setImage(null);
        setVideo(null);
        setAudio(null);
    };
  
    return (
        <WidgetWrapper>
            <FlexBetween>
                <FlexBetween gap="0.25rem" onClick={() => {
                    setIsText(!isText)
                    setIsImage(false)
                    setIsVideo(false)
                    setIsAudio(false)
                    }}>
                    <NotesOutlined sx={{ color: mediumMain }} />
                    <Typography 
                        color={mediumMain}
                        sx={{ "&:hover": { cursor: "pointer", color: medium } }}
                    >
                        Text
                    </Typography>
                </FlexBetween>

                <FlexBetween gap="0.25rem" onClick={() => {
                    setIsText(false)
                    setIsImage(!isImage)
                    setIsVideo(false)
                    setIsAudio(false)
                    }}>
                    <ImageOutlined sx={{ color: mediumMain }} />
                    <Typography
                        color={mediumMain}
                        sx={{ "&:hover": { cursor: "pointer", color: medium } }}
                    >
                        Image
                    </Typography>
                </FlexBetween>

                {isNonMobileScreens ? (
                <>
                    <FlexBetween gap="0.25rem" onClick={() => {
                        setIsText(false)
                        setIsImage(false)
                        setIsVideo(!isVideo)
                        setIsAudio(false)
                        }}>
                    <VideocamOutlined sx={{ color: mediumMain }} />
                    <Typography 
                        color={mediumMain}
                        sx={{ "&:hover": { cursor: "pointer", color: medium } }}
                    >
                        Video
                    </Typography>
                    </FlexBetween>

                    <FlexBetween gap="0.25rem" onClick={() => {
                        setIsText(false)
                        setIsImage(false)
                        setIsVideo(false)
                        setIsAudio(!isAudio)
                        }}>
                    <MicOutlined sx={{ color: mediumMain }} />
                    <Typography 
                        color={mediumMain}
                        sx={{ "&:hover": { cursor: "pointer", color: medium } }}
                    >
                        Audio
                    </Typography>
                    </FlexBetween>
                </>
                ) : (
                <FlexBetween gap="0.25rem">
                    <MoreHorizOutlined sx={{ color: mediumMain }} />
                </FlexBetween>
                )}
            </FlexBetween>

            <Divider sx={{ margin: "1.25rem 0" }} />
                        
            {isText && (
                <FlexBetween gap="1.5rem">
                    <InputBase
                    placeholder="Enter text here..."
                    multiline={true}
                    onChange={(e) => setText(e.target.value)}
                    value={text}
                    sx={{
                        width: "100%",
                        backgroundColor: palette.neutral.light,
                        borderRadius: "1rem",
                        padding: "1rem 2rem",
                    }}
                    />
                </FlexBetween>
            )}
            {isImage && (
                <Box
                border={`1px solid ${medium}`}
                borderRadius="5px"
                mt="1rem"
                p="1rem"
                >
                <Dropzone
                    accept=".jpg,.jpeg,.png"
                    multiple={false}
                    onDrop={(acceptedFiles) => setImage(acceptedFiles[0])}
                >
                    {({ getRootProps, getInputProps }) => (
                    <FlexBetween>
                        <Box
                            {...getRootProps()}
                            border={`2px dashed ${palette.primary.main}`}
                            p="1rem"
                            width="100%"
                            sx={{ "&:hover": { cursor: "pointer" } }}
                        >
                        <input {...getInputProps()} />
                        {!image ? (
                            <p>Add Image Here</p>
                        ) : (
                            <FlexBetween>
                            <Typography>{image.name}</Typography>
                            <EditOutlined />
                            </FlexBetween>
                        )}
                        </Box>
                        {image && (
                        <IconButton
                            onClick={() => setImage(null)}
                            sx={{ width: "15%" }}
                        >
                            <DeleteOutlined />
                        </IconButton>
                        )}
                    </FlexBetween>
                    )}
                </Dropzone>
                </Box>
            )}
            {isVideo && (
                <Box
                border={`1px solid ${medium}`}
                borderRadius="5px"
                mt="1rem"
                p="1rem"
                >
                <Dropzone
                    accept=".avi,.wmv,.mp4"
                    multiple={false}
                    onDrop={(acceptedFiles) => setVideo(acceptedFiles[0])}
                >
                    {({ getRootProps, getInputProps }) => (
                    <FlexBetween>
                        <Box
                            {...getRootProps()}
                            border={`2px dashed ${palette.primary.main}`}
                            p="1rem"
                            width="100%"
                            sx={{ "&:hover": { cursor: "pointer" } }}
                        >
                        <input {...getInputProps()} />
                        {!video ? (
                            <p>Add Video Here</p>
                        ) : (
                            <FlexBetween>
                            <Typography>{video.name}</Typography>
                            <EditOutlined />
                            </FlexBetween>
                        )}
                        </Box>
                        {video && (
                        <IconButton
                            onClick={() => setVideo(null)}
                            sx={{ width: "15%" }}
                        >
                            <DeleteOutlined />
                        </IconButton>
                        )}
                    </FlexBetween>
                    )}
                </Dropzone>
                </Box>
            )}
            {isAudio && (
                <Box
                border={`1px solid ${medium}`}
                borderRadius="5px"
                mt="1rem"
                p="1rem"
                >
                <Dropzone
                    accept=".wav,.mp3"
                    multiple={false}
                    onDrop={(acceptedFiles) => setAudio(acceptedFiles[0])}
                >
                    {({ getRootProps, getInputProps }) => (
                    <FlexBetween>
                        <Box
                            {...getRootProps()}
                            border={`2px dashed ${palette.primary.main}`}
                            p="1rem"
                            width="100%"
                            sx={{ "&:hover": { cursor: "pointer" } }}
                        >
                        <input {...getInputProps()} />
                        {!audio ? (
                            <p>Add Audio Here</p>
                        ) : (
                            <FlexBetween>
                            <Typography>{audio.name}</Typography>
                            <EditOutlined />
                            </FlexBetween>
                        )}
                        </Box>
                        {audio && (
                        <IconButton
                            onClick={() => setAudio(null)}
                            sx={{ width: "15%" }}
                        >
                            <DeleteOutlined />
                        </IconButton>
                        )}
                    </FlexBetween>
                    )}
                </Dropzone>
                </Box>
            )}

            <FlexBetween justifyItems="center">
                <Button
                    disabled={!((text && isText) || (image && isImage) || (video && isVideo) || (audio && isAudio))}
                    onClick={handlePost}
                    sx={{
                        color: palette.background.alt,
                        backgroundColor: palette.primary.main,
                        borderRadius: "0.5rem",
                        mt: "1rem",
                        width: "100%"
                    }}
                    >
                    Submit
                </Button>
            </FlexBetween>
        </WidgetWrapper>
    );
};
  
export default InputPostWidget;