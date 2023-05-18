function get_Y_axis(list) {
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
            <label for="y_axis"> Y axis:
                <select id='y_axis' name="y">
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
export default get_Y_axis;