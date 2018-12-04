import React from "react";
import { View, Text, AsyncStorage, SectionList, FlatList, Button } from "react-native";
import { Card, FAB, Portal, Provider } from "react-native-paper";

import BasicScreen from './BasicScreen'
import styles from './styles'
import { root, dashboard, authenticate } from './RouteConfigs'

export const dashboardLink = root+dashboard;
export const authLink = root+authenticate;

const theme = {
    colors: {
        primary: '#3DBE98',
        accent: '#03dac4',
        background: '#3DBE98',
        surface: '#ffffff',
        error: '#be3d63',
        text: '#E5E5E5',
    },
};

export default class MainScreen extends BasicScreen {
    static navigationOptions = {
        title: 'Dashboard',
        headerTitleStyle: {
            textAlign: 'center', alignSelf: 'center', color: '#FFFFFF'
        },
    };
    constructor(props) {
        super(props);
        this.state = {
            userInfo: null,
            dashboardResponse: null,
            authToken: null,
            sections: [
                { title: 'Flashcards', data: [{key: this._cardsList}] },
                { title: 'Sessions', data: [] }
            ],
            flashcards: { keys: [{key: 'a'}] },
            sessions: { key: [{key: 'a'}] },
            test: 1,
            addToggle: false,
            cardOut: '1'
        };
    }

    _card = (contents) => {
        return (
            <Card style={styles.dashCardDisplay}>
                <Card.Content>
                    <Text>{contents}</Text>
                </Card.Content>
            </Card>
        )
    };

    _cardsList = () => {
        return <FlatList
                horizontal={true}
                data={this.state.flashcards.keys}
                extraData={this.state}
                renderItem={ ({item}) => this._card(item.key) }
        />
    };

    _addCard = () => {
        console.log('pressed');
        let cards = this.state.flashcards;
        let value = this.state.test++;
        cards.keys.push({ key: String(value) });
        this.setState({ flashcards: cards });
        console.log(this.state);
    };

    _handleNewFlashcard = () => { this.props.navigation.navigate('Capture') };

    render() {
        return(
            <View style={styles.container}>
                <View style={styles.container}>
                    <SectionList
                        renderItem={() => this._cardsList() }
                        renderSectionHeader={ ({ section: { title } }) => (<Text style={styles.dashSectionHeader}>{title}</Text>) }
                        sections={ this.state.sections }
                        keyExtractor={ (item, index) => item + index }
                    />
                    <Provider>
                        <Portal>
                            <FAB.Group
                                open={ this.state.addToggle }
                                icon="add"
                                actions={[
                                    { icon: 'star', label: 'New Flashcards', onPress: () => { this._handleNewFlashcard() }},
                                    { icon: 'notifications', label: 'New Session', onPress: () => console.log('new session option pressed. ')}
                                ]}
                                onStateChange={ ({ open }) => this.setState({ addToggle: open }) }/>
                        </Portal>
                    </Provider>
                </View>
            </View>
        );
    }

    componentWillMount() {
         AsyncStorage.getItem('authToken').then((value) => {
             this.confirmAuthorization(value);
         }).done()
    };

    componentDidMount() {
        AsyncStorage.getItem('authToken').then((value) => {
            this.setState({ authToken: value });
            return value;
        }).then((value) => { this.requestDashboardData(value) }).done();
    };

    requestDashboardData = (token) => {
        const body = JSON.stringify({ data: 'Request to Dashboard from client', jwtAuth: token });
        this.makeRequest(dashboardLink, body, token)
            .then((response) => { return response.json() })
            .then((responseJson) => {
                this.setState({ dashboardResponse: responseJson });
            }).done();
    };

    /* Makes request to server with token, to check if that token's valid. */
    confirmAuthorization = (token) =>  {
        console.log('passed token: '+token);
        console.log(this.state);
        let body = JSON.stringify({ jwtAuth : token });
        this.makeRequest(authLink, body, token)
            .then(response => { return response.json() })
            .then(jsonResponse => {
                console.log(jsonResponse);
                if (jsonResponse['error'] === true) {
                    throw jsonResponse['message'];
                }
            }).catch(error => {
                console.log("error: "+error);
            });
    };

    makeRequest = (url, body, auth) => {
        return fetch (url, {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
                'Authorization': auth,
            },
            body: body,
            credentials: 'same-origin'
        })
    };
}

