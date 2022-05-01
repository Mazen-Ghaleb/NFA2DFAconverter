mergeInto(LibraryManager.library, {
  fromUnityDisplayDFA: function (str) {
    window.displayDFA(UTF8ToString(str));
    // tab = window.open("./display.html?nfa=" + str, '_blank')
    // if(tab) tab.focus();
  },
});
