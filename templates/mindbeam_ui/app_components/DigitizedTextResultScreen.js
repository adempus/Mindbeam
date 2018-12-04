import React from 'react';
import { Text, TextInput, View, ScrollView, Button, } from 'react-native';

import {root, textUpload } from './RouteConfigs'

export default class DigitizedTextResultScreen extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            digitizedText: this.props.navigation.getParam('digitizedText', null),
        };
    };

    handleConfirmButton = () => {
        this.props.navigation.navigate('Loading', { text: this.state.digitizedText })
    };

    handleRetakeButton = () => { this.props.navigation.navigate('Capture') };

    render() {
        return(
            <View style={styles.container}>
                <ScrollView style={{ flex: 1 }}>
                    <TextInput title="Response Text" multiline={true} >
                        <Text style={{flexWrap: "wrap", textAlignVertical: 'center'}}>{this.state.digitizedText}</Text>
                    </TextInput>
                </ScrollView>
                <View style={{ flex: 1 }}>
                    <Button title="confirm" onPress={() => this.handleConfirmButton()  }/>
                    <Button title="retake" onPress={() => this.handleRetakeButton()  }/>
                </View>
            </View>
        );
    };
};
