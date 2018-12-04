using ReactNative.Bridge;
using System;
using System.Collections.Generic;
using Windows.ApplicationModel.Core;
using Windows.UI.Core;

namespace Mindbeam.Lib.RNMindbeamLib
{
    /// <summary>
    /// A module that allows JS to share data.
    /// </summary>
    class RNMindbeamLibModule : NativeModuleBase
    {
        /// <summary>
        /// Instantiates the <see cref="RNMindbeamLibModule"/>.
        /// </summary>
        internal RNMindbeamLibModule()
        {

        }

        /// <summary>
        /// The name of the native module.
        /// </summary>
        public override string Name
        {
            get
            {
                return "RNMindbeamLib";
            }
        }
    }
}
