
import React from 'react';
import { Text, View, Button, CameraRoll } from 'react-native';
import Expo, { Camera, Permissions, } from 'expo';


export default class DocumentCaptureScreen extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            hasCameraPermission: null,
            hasFileSystemPermission: null,
            type: Camera.Constants.Type.back,
            photoURI: null
        }
    };

    componentDidMount = async () => {
        const { cameraPermission } = await Permissions.askAsync(Permissions.CAMERA);
        const { albumAccessPermission } = await Permissions.askAsync(Permissions.CAMERA_ROLL);
        this.setState({ hasCameraPermissions: cameraPermission === 'granted' });
        this.setState({ hasFileSystemPermissions: albumAccessPermission === 'granted' });
    };

    render() {
        return (
            <View style={{ flex: 1 }}>
                <Camera ref={(ref) => { this.camera = ref }}
                        style={{ flex: 1 }}
                        type={ this.state.type }
                        autoFocus={ 'on' }
                />
                <Button title='Capture' style={{ height: 100 }} onPress={() => {
                    this._captureDocument().then(() => { this.navigateCapturePreview() }).done()}}
                />
            </View>
        );
    };

    // sample text: doc = nlp(u' In addition to an IP address, every device on a network running IPv4 is assigned a sub-net mask. A subnet mask is a special 32-bit number the IP address, informs the rest of the network about the segment or network to which the device is attached. That is, it identifies the device\'s subnet. Like IP addresses, subnet masks are composed of four octets (32 bits) and can be expressed in either binary or dotted decimal notation. ')
    _captureDocument = async () => {
        if (this.camera) {
            let photo = await this.camera.takePictureAsync();
            this.setState({ photoURI: photo.uri });
            console.log('photo saved to state. \n'+this.state)
        }
    };

    navigateCapturePreview = () => {
        console.log("navigating to capture preview. ");
        this.props.navigation.navigate('Preview', { docImage: this.state.photoURI });
    }
};