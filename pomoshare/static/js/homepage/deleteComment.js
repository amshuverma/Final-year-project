function deleteComment(){
    return{
        async deleteComment(url, pk){
            data = {'pk': pk}
            const response = fetch(url, {
                method: 'POST',
                body: JSON.stringify(data),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': cookie,
                }
            })

            return response
        }
        }
    }