import React from "react";
import { View, Text, AsyncStorage } from "react-native"
import { Button, TextInput, HelperText } from "react-native-paper"
import { AppLoading } from "expo"

import BasicScreen from './BasicScreen'
import { root, signIn, authenticate } from './RouteConfigs'
import styles from './styles'

export const signInLink = root+signIn;
export const verifyAuthLink = root+authenticate;

export default class SignInScreen extends BasicScreen {
    constructor(props) {
        super(props);
        this.state = {
            tries: 1,
            emailField: "",
            passwordField: "",
            signInResponse: null,
            signInSuccess: false,
            errorMessages: new Array(2),
            token: null
        };
    }

    // updates respective states when TextInput is changed by the user.
    handleEmailFieldChange = event => { this.setState({ emailField: event.nativeEvent.text }) };
    handlePasswordFieldChange = event => { this.setState({ passwordField: event.nativeEvent.text }) };

    render() {
        if (!this.state.isReady) { return <AppLoading/>; }
        return (
                <View style={styles.container}>
                    <Text style={styles.titleTxt}>Sign In</Text>
                    <View>
                        <TextInput mode="outlined"
                                   style={{width: 300, height: 50, marginTop: 25, marginBottom: 5, borderColor: "#ffffff"}}
                                   label='email'
                                   onChange={this.handleEmailFieldChange}/>
                        <HelperText type ="error" visible={this.state.errorMessages[0] !== null} style={styles.errorText} >
                            { this.state.errorMessages[0] }
                        </HelperText>
                    </View>
                    <View>
                        <TextInput mode="outlined"
                                   style={{width: 300, height: 50, marginTop: 8, marginBottom:5}}
                                   label='password'
                                   secureTextEntry={true}
                                   onChange={this.handlePasswordFieldChange}/>
                        <HelperText type ="error" visible={this.state.errorMessages[1] !== null} style={styles.errorText}>
                            {this.state.errorMessages[1]}
                        </HelperText>
                    </View>
                    <Button mode="outlined" style={styles.frontButtons} onPress={() => this.handleLogin()}>
                        <Text style={{color: "#FFFFFF"}}>
                            Login
                        </Text>
                    </Button>
                    <Button mode="outlined" style={styles.frontButtons} onPress={() => this.handleSignUpPress()}>
                        <Text style={{color: '#FFFFFF'}}>New User?</Text>
                    </Button>
                    <HelperText type ="info" visible={this.state.signInSuccess === true}
                                style={{color: "#ebf8f4", fontFamily: 'K2D-LightItalic', marginTop: 10}} >
                        Successfully logged in!
                    </HelperText>
                </View>
        );
    }

    handleLogin() {
        console.log('login button pressed ');
        console.log(this.state);
        return fetch (signInLink, {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: this.state.emailField,
                password: this.state.passwordField,
            }),
            credentials: 'same-origin'
        })
            .then(response => { return response.json() })
            .then(jsonResponse => {
                this.setState({signInResponse: jsonResponse});
                console.log(this.state['signInResponse']);
                this.setValidationState();
                // noinspection JSIgnoredPromiseFromCall
                this.localPersistAuthToken();
            }).done();
    }

    localPersistAuthToken = async() => {
        let token = null;
        if (this.state.signInSuccess) {
            token = this.state['signInResponse'].token;
        }
        await AsyncStorage.setItem('authToken', token);
        this.props.navigation.navigate('MainApp', { title: 'Dashboard' });
    };

    setValidationState() {
        this.setState({ signInSuccess: !this.state['signInResponse'].error });
        this.setState({ errorMessages: this.state['signInResponse'].messages });
    }

    handleSignUpPress() {
        console.log('Route to sign up.');
        this.props.navigation.navigate('SignUp');
    }
}
