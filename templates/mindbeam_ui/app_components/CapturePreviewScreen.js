import React from 'react'
import { View, ScrollView, Button, Image, Dimensions } from 'react-native';

import styles from './styles'

export default class CapturePreviewScreen extends React.Component {
    constructor(props) {
        super(props);
        this.state = { image: this.props.navigation.getParam('docImage', null) };
        this.printImgUri();
    }

    printImgUri = () => {
        console.log("image uri: "+this.state.image);
    };

    render() {
        return(
            <View style={styles.component}>
                <ScrollView>
                    <Image
                        style={{
                            width: Dimensions.get('window').width,
                            height: Dimensions.get('window').height-145
                        }}
                        source={{ uri: this.state.image }} />
                </ScrollView>
                <View style={{marginBottom: 1 }} >
                    <Button title="confirm" onPress={() => { this.confirm() }}>
                    </Button>
                </View>
                <View>
                    <Button title="retake" onPress={() => { this.retake() }}>
                    </Button>
                </View>
            </View>
        );
    }

    retake = () => { this.props.navigation.navigate('Capture') };
    confirm = () => { this.props.navigation.navigate('Loading', { image: this.state.image })};
}