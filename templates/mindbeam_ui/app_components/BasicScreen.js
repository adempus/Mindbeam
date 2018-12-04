import React from "react";
import {Font} from "expo";

/** Class for loading basic fonts loaded from Start component contains isReady state. **/
class BasicScreen extends React.Component {
    state = { isReady: false };
    componentWillMount() {
        // this function promises to load the fonts below
        (async() => {
            await Font.loadAsync({'K2D-Regular' : require('../assets/fonts/K2D/K2D-Regular.ttf')});
            await Font.loadAsync({'K2D-Medium' : require('../assets/fonts/K2D/K2D-Medium.ttf')});
            await Font.loadAsync({'K2D-Bold' : require('../assets/fonts/K2D/K2D-Bold.ttf')});
            await Font.loadAsync({'K2D-SemiBold' : require('../assets/fonts/K2D/K2D-SemiBold.ttf')});
            await Font.loadAsync({'K2D-LightItalic' : require('../assets/fonts/K2D/K2D-LightItalic.ttf')});
            await Font.loadAsync({'Roboto_medium' : require('../assets/fonts/Roboto/Roboto_medium.ttf')});
            this.setState({ isReady : true });
        })();
    }
}

export default BasicScreen;