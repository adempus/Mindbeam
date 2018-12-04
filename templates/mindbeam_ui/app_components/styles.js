import { StyleSheet } from "react-native";

export default styles = StyleSheet.create({
    container: {
        flex: 1,
        paddingTop: 0,
        flexDirection: 'column',
        // justifyContent: 'space-around',
        alignSelf: 'stretch',
        alignItems: 'center',
        // placeContent: 'space-around-start',
        backgroundColor: '#3DBE98'
    },
    titleTxt: {
        color: '#E5E5E5',
        fontSize: 36,
        fontFamily: 'K2D-Regular'
    },
    startButtons: {
        borderWidth: 1,
        paddingLeft: 45, paddingRight: 45, paddingTop: 10, paddingBottom: 10,
        fontSize: 20,
        // fontWeight: 'bold',
        borderRadius: 10,
        elevation: 3,
        color: '#E5E5E5',
        borderColor: '#E5E5E5',
        backgroundColor: '#3DBE98',
        fontFamily: 'K2D-Medium'
    },
    frontButtons: {
        backgroundColor: '#3DBE98',
        // fontFamily: 'K2D-Medium',
        borderColor: "#FFFFFF",
        // color: "#FFFFFF",
        height: "10%",
        paddingTop: 5,
        width: "40%",
        marginTop: '5%'
    },
    txtInputLabel: {
        fontFamily: 'K2D-Medium',
        color: '#FFFFFF',
        fontSize: 14,
        marginBottom: 5,
        textAlign: 'left'
    },
    txtInput: {
        width: '70%',
        height: '6.5%',
        // backgroundColor: '#62ccad',
        // elevation: .5,
        // fontSize: 17,dd
        // marginTop: 10,
        // marginBottom: 1,
        // paddingLeft: 7,
        // paddingRight: 7,
        // letterSpacing: .2,
        fontFamily: 'K2D-Regular',
        // borderColor: '#62ccad',
        borderColor: '#FFFFFF',
        // borderRadius: 7,
        color: '#ffffff'
    },
    errorText: {
        color: '#be3d63',
        fontFamily: 'K2D-LightItalic',
        padding: 0,
        alignSelf: 'stretch'
    },
    successText: {
        color: '#ebf8f4',
        fontFamily: 'K2D-LightItalic'
    },
    // styles for Dashboard
    dashSectionHeader: {
        fontSize: 15,
        fontWeight: "bold",
        color: "#3DBE98",
        paddingTop: 7,
        paddingLeft: 10,
        marginBottom: 10,
        marginLeft: 3,
        borderWidth: 1,
        height: 35,
        width: 355,
        borderColor: '#e5e5e5',
        backgroundColor: "#FFFFFF",
    },
    dashCardDisplay: {
        width: 225,
        height: 130,
        paddingTop: 5,
        marginBottom: 30,
        marginLeft: 35,
        marginTop: 20
    },
    newCardButton: {
        marginBottom: '7%',
        marginLeft: '71%',
        // backgroundColor: '#EEEEEE'
    },
    loadingScreenContainer: {
        backgroundColor: '#ebf8f4',
        flex: 1,
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'stretch'
    }
    // blankFlashcardCanvas : {
    //
    // }
});