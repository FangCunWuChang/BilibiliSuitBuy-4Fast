(async function() {
    const config = await getLocalContent("config") || {"style": {}};
    const style = config["style"];
    
    document.body.style.backgroundColor = style["popup-background-color"];
})();
