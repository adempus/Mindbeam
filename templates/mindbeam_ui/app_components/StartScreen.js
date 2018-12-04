import React from "react";
import {Text, TouchableOpacity, View} from "react-native";
import { Provider as PaperProvider} from 'react-native-paper';
import {AppLoading} from "expo";

import BasicScreen from './BasicScreen';

export default class StartScreen extends BasicScreen {
    render() {
        if (!this.state.isReady) { return <AppLoading />; }
        return (

                <View style={styles.container}>
                    <View style={{ justifyContent: 'space-around', marginTop: '10%', marginBottom: 100, paddingBottom: 25 }}>
                        <Text style={styles.titleTxt}>Mindbeam™</Text>
                    </View>
                    <View style={{ marginBottom: 25 }}>
                        <TouchableOpacity onPress={() => this.handleSignIn() }>
                            <Text style={styles.startButtons}>Sign In </Text>
                        </TouchableOpacity>
                    </View>
                    <View>
                        <TouchableOpacity onPress={() => this.handleSignUp() }>
                            <Text style={styles.startButtons}>Sign Up</Text>
                        </TouchableOpacity>
                    </View>
                </View>
            // </PaperProvider>
        );
    }
    handleSignIn() {
        this.props.navigation.navigate('SignIn');
        console.log('Sign-in button pressed.');
    }
    handleSignUp() {
        // Alert.alert('Sign-up button pressed.');
        this.props.navigation.navigate('SignUp');
        console.log('Sign-up button presses.');
    }
}