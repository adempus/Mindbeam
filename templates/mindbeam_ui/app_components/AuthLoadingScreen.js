import React from "react";
import { AsyncStorage, View, Text } from 'react-native';

export default class AuthLoadingScreen extends React.Component {
    constructor(props) {
        super(props);
        // noinspection JSIgnoredPromiseFromCall
        this._initTokenStore();
    }

    // retrieve valid JSON web token to store locally, from a non-erroneous authToken response.
    _initTokenStore = async() => {
        const authToken = await AsyncStorage.getItem('authToken');
        // make the switch to user Dashboard screen on valid token, else force re-authToken on error.
        this.props.navigation.navigate(authToken ? 'MainApp' : 'Auth');
    };

    render() {
        return(
            <View>
                <Text> Loading Authentication </Text>
            </View>
        );
    }
}