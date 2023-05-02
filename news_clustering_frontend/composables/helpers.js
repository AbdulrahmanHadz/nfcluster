export function isNumeric(num) {
    return !isNaN(num);
};


export function capitalise(s) {
    return s && s[0].toUpperCase() + s.slice(1);
};

export function randomColour() {
    return Math.floor(Math.random() * 16777215).toString(16);
}

export function generateRandomColoursArray(data) {
    const colours = [];
    for (let i = 0; i < Object.keys(data).length; i++) {
        const colour = randomColour();
        colours.push(`#${colour}`);
    }
    return colours;
}

export function updateUrl(query) {
    const newParams = { ...useRoute().query, ...query }
    router.replace({
        query: newParams
    })
}

export function getKeyByValue(object, value) {
    return Object.keys(object).find(key => object[key] === value);
}