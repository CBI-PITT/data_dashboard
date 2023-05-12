function get_GroupBy(list) {
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
            <div>
                <h2>Group By</h2>
                <label for="groupBy">
                    <select id='groupBy' name="group_by" multiple size={3}>
                        {
                            list.map((item) => (
                                <option value={item}>{item}</option>
                            ))
                        }
                    </select>
                </label>

            </div>
        )
    }
}

export default get_GroupBy;