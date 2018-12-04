import React from 'react'
import { View, Text, AsyncStorage, ActivityIndicator } from 'react-native'

import styles from './styles'
import {root, imageUpload, textUpload} from './RouteConfigs'

const imgUploadLink = root+imageUpload;
const textUploadLink = root+textUpload;
const indent = '\n\t\t\t';
const loadingMessages = [
    'The extracted text will be available for you to edit.',
    'You may then select passages of text to'+indent+'questionize into flashcards.',
    'You can also customize your flashcards'+indent+'into question types and categories.',
    'Create study sessions to review flashcards you\'ve made,'+indent+'using the proven Leitner system.',
    'Finalizing...'
];

export default class LoadingScreen extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            image: this.props.navigation.getParam('image', null),
            text: this.props.navigation.getParam('text', null),
            auth: null,
            uploadResponse: null,
            currentMessage: 'Uploading image for text extraction. Please wait...',
        };
    }

    componentDidMount() {
        AsyncStorage.getItem('authToken').then((value) => {
            this.setState({auth: value});
        }).then(() => {
            try {
                if (this.state.image !== null) {
                    this.makeRequest();
                } else {
                    this.makeTextRequest();
                    // console.log('one full step for a man');
                }
            } catch (err) {
                console.log("An error occurred. Navigating back to capture preview."+err);
                this.props.navigation.navigate('Preview', { docImage: this.state.image });
            }
        }).done();
        let index = 0;
        this.interval = setInterval(() => {
            this.setState({ currentMessage: loadingMessages[index++]} )}, 5000)
    };

    componentWillUnmount() {
        clearInterval(this.interval);
    }

    render() {
        return(
            <View style={styles.loadingScreenContainer}>
                <View style={{paddingTop: 200}}>
                    <ActivityIndicator size={55} color="#3DBE98"/>
                </View>
                <View style={{flex: 1}}>
                    <Text title='upload status' style={{
                        color: '#3DBE98', fontSize: 12, marginTop:25, alignSelf: 'center', alignItems: 'center' }}>
                        {this.state.currentMessage}
                    </Text>
                </View>
            </View>
        )
    };

    getTimestamp = () => { return new Date().toDateString()+" "+new Date().toLocaleTimeString() };

    makeTextRequest = () => {
        fetch(textUploadLink, {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Authorization': this.state.auth,
            },
            body: JSON.stringify({
                confirmedDoc: this.state.digitizedText
            }),
            credentials: 'same-origin'
        }).then(response => {
            return response.json()
        }).then(responseJson => {
            console.log(responseJson);
        }).done();
    };

    makeRequest = () => {
        let formData = new FormData();
        formData.append('photo', {
            uri: this.state.image,
            type: 'image/jpeg',
            name: this.getTimestamp()+'.jpg'
        });

        fetch(imgUploadLink, {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Authorization': this.state.auth,
            },
            body: formData,
            credentials: 'same-origin'
        })
            .then(response => { return response.json() })
            .then(jsonResponse => { this.setState({ uploadResponse: jsonResponse })})
            .then(() => {
                console.log("messages: "+this.state['uploadResponse'].messages[0]);
                let digitizedTxt = this.state.uploadResponse.data.digitizedText;
                console.log("Digitized text: \n"+digitizedTxt);
                this.props.navigation.navigate('Results', {'digitizedText': digitizedTxt });
            }).done();
    };
};