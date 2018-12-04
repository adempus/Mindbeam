import React from "react";
import {View, Text, AsyncStorage } from "react-native"

import styles from './styles'

export default class SentenceSelectionScreen extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            digitizedText: this.props.navigation.getParam('digitizedText', null),
            sentencizedResponse: null,
        }
    };



    render() {
        return (
            <View style={styles.container}>
                <Text title="Sentencized text"/>
            </View>
        );
    }
};
