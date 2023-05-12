function get_Aggregation(list) {
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
            <label for="aggregation">Aggregation:
                <select id='aggregation' name="aggregate" >
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

export default get_Aggregation;