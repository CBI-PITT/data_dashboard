function getCate(key, value) {
    // const key = ["Treatment", "Time_Point"]
    // const value = [["eeve", "weev", "vvev"], [24, 48, 72, 96]]
    if (key !== undefined && value !== undefined) {

        return (
            // current like{"treatment" : ["weev","veev"]}
            // should be packed to "filter": {
            //     "categorical": {"<column_name>": [<value1>, <value2>], "<column_name>": [<value1>, <value2>]},
            //     "continuous": {"<column_name>": [<min>, <max>], "<column_name>": [<min>, <max>]}
            // }
            <div>
                {
                    key.map((k, ind) => (
                        <div>
                            <h2>{k}</h2>
                            <label for={k}>
                                {/* {console.log(k)} */}
                                <select id={k} name={k} size={3} multiple>
                                    {value[ind].map((v) => (
                                        <option value={v}>
                                            {v}
                                        </option>
                                    ))}
                                </select>
                            </label>
                        </div>
                    ))
                }
            </div>
        )
    }
}

export default getCate;