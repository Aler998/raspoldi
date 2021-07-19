const mergeAndSort = (arr1, arr2) => {
    const merged = arr1.concat(arr2)
    console.log(merged)
    const newArr = []

    let minDate = new Date(merged[0].created_at)
    let maxDate = new Date(merged[0].created_at)

    merged.forEach(element => {
        let dat = new Date(element.created_at)
        if (dat >= maxDate) {
            newArr.unshift(element)
            maxDate = dat
        }
        if (dat < minDate) {
            newArr.push(element)
            minDate = dat
        }
    });

    while (merged.length() > 11) {
        merged.pop()
    }

    return newArr
}

module.exports = mergeAndSort