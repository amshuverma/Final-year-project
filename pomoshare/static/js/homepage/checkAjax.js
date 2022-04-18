function handleNav(){
    return {
        checkActiveUrl(url){
            const splitUrl = url.split('/');
            let activeUrl = ''
            if (length(activeUrl) === 4){
                activeUrl = 'home';
            }
            else if (length(activeUrl) === 5){
                activeUrl = splitUrl[3];
            }
        },

        currentUrl: window.location.href,
        activeUrl: checkActiveUrl(currentUrl),
    }
}