import { createSwitchNavigator, createStackNavigator } from 'react-navigation'
import React from 'react';

import StartScreen from './app_components/StartScreen'
import SignInScreen from './app_components/SignInScreen'
import SignUpScreen from './app_components/SignUpScreen'
import MainScreen from './app_components/MainScreen'
import DocumentCaptureScreen from './app_components/DocumentCaptureScreen'
import CapturePreviewScreen from  './app_components/CapturePreviewScreen'
import AuthLoadingScreen from './app_components/AuthLoadingScreen'
import LoadingScreen from './app_components/LoadingScreen'
import DigitizedTextResultScreen from './app_components/DigitizedTextResultScreen'
import SentenceSelectionScreen from './app_components/SentenceSelectionScreen'

let navigationOptions = {
    headerStyle: { backgroundColor: '#3DBE98' }
};

const AppStack = createStackNavigator({ Main: MainScreen, Capture: DocumentCaptureScreen, Preview: CapturePreviewScreen,
    Loading: LoadingScreen, Results: DigitizedTextResultScreen, SentenceSelect: SentenceSelectionScreen }, { navigationOptions });

const AuthStack = createStackNavigator({ Start: StartScreen, SignIn: SignInScreen, SignUp: SignUpScreen}, { navigationOptions });
App = createSwitchNavigator(
    {
        AuthLoading: AuthLoadingScreen,
        MainApp: AppStack,
        Auth: AuthStack
    },
    { initialRouteName: 'Auth', },
    // withNavigation(StartScreen , SignInScreen, SignUpScreen)
);

export default App;
