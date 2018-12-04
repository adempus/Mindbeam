import React from "react";
import { View, Text } from 'react-native';
import { TextInput, Button, HelperText } from 'react-native-paper'
import  { root, signUp } from './RouteConfigs'
import styles from './styles';

export const signUpLink = root+signUp;
export default class SignUpScreen extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            username: "",
            email:    "",
            password: "",
            confirmPass: "",
            validEmail: null,
            validPassword: null,
            validUsername: null,
            errorMessages: new Array(2),
            response: "",
        };
    }

    render() {
        return (
            <View style={styles.container}>
                <Text style={styles.titleTxt}>Sign Up</Text>
                <View>
                    <TextInput mode="outlined"
                               style={{width: 300, height: 50, marginTop: 2, borderColor: "#ffffff"}}
                               label='username'
                               onChange={this.handleUsernameFieldChange}/>
                    <HelperText name='help' type="error" visible={this.state.username === ""} style={styles.errorText}>
                        username is empty
                    </HelperText>
                </View>
                <View>
                    <TextInput mode="outlined"
                               style={{width: 300, height: 50, marginTop: 2, marginBottom: 0, borderColor: "#ffffff"}}
                               label='email'
                               onChange={this.handleEmailFieldChange}/>
                    <HelperText type="error" visible={this.state.validEmail === false} style={styles.errorText}>
                        {this.state.errorMessages[0]}
                    </HelperText>
                </View>
                <View>
                    <TextInput mode="outlined"
                               style={{width: 300, height: 50, marginTop: 2, marginBottom: 20, borderColor: "#ffffff"}}
                               label='password'
                               secureTextEntry={true}
                               onChange={this.handlePasswordFieldChange}
                    />
                    <TextInput mode="outlined"
                               style={{width: 300, height: 50, marginTop: 8, marginBottom: 0, borderColor: "#ffffff"}}
                               label='Confirm password'
                               secureTextEntry={true}
                               onChange={ this.handleConfirmPasswordFieldChange }
                    />
                    <HelperText type="error" visible={this.state.validPassword === false} style={styles.errorText}>
                        {this.state.errorMessages[1]}
                    </HelperText>
                </View>
                <Button mode="outlined" style={styles.frontButtons} onPress={() => this.handleContinue()}>
                    <Text style={{color: '#FFFFFF'}}>Continue</Text>
                </Button>
            </View>
        );
    }

    handleUsernameFieldChange = event => { this.setState({ username: event.nativeEvent.text }) };
    handleEmailFieldChange = event => { this.setState({email: event.nativeEvent.text }) };
    handlePasswordFieldChange = event => { this.setState({password: event.nativeEvent.text }) };
    handleConfirmPasswordFieldChange = event => { this.setState({confirmPass: event.nativeEvent.text}) };

    handleEmailInputDone() {
        console.log(this.state.username);
    }

    handleContinue() {
        this.setRegistrationResponse();
    }

    setRegistrationResponse() {
        return fetch(signUpLink, {
            method: 'POST',
            headers : {
                Accept: 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: this.state.username,
                email: this.state.email,
                password: this.state.password,
                confirmPass: this.state.confirmPass,
            }),
            credentials: 'same-origin'
        })
            .then(response => { return response.json() })
            .then(responseJson => {
                this.setState({ response: responseJson });
                return this.isSignUpInfoValid();
            });
    }

    isSignUpInfoValid() {
        console.log(this.state['response']);
        let emailNotValid = this.state['response'].messages[0] !== null;
        let passNotValid = this.state['response'].messages[1] !== null;
        let eitherOrInvalid = this.state['response'].error === true  && (emailNotValid || passNotValid);

        if (eitherOrInvalid) {
            let errMsgArray = this.state.errorMessages;
            if (emailNotValid) {
                this.setState({ validEmail: false });
                errMsgArray[0] = this.state['response'].messages[0];
                this.setState({ errorMessages: errMsgArray });
            } else {
                this.setState({validEmail: true});
            }

            if (passNotValid) {
                this.setState({ validPassword: false });
                errMsgArray[1] = this.state['response'].messages[1];
                this.setState({ errorMessages: errMsgArray });
            } else {
                this.setState({validPassword: true})
            }
            return eitherOrInvalid;
        }
        return false;
    }
}