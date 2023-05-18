function get_X_axis(list) {
    // console.log(list)
    if (list !== undefined) {
        return (
            // <div>
            //     {
            //         list.map((item) => (
            //             <span>
            //                 {item} /
            //             </span>
            //         ))
            //     }
            // </div>
            <label for="x_axis"> X axis:
                <select id='x_axis' name="x">
                    {
                        list.map((item) => (
                            <option value={item}>{item}</option>
                        ))
                    }
                </select>
            </label>
        )
    }
}

export default get_X_axis;