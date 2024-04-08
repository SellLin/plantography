/*
 * @Description: 
 * @Author: Qing Shi
 * @Date: 2022-11-20 19:23:35
 * @LastEditTime: 2023-01-27 09:25:19
 */

import axios from 'axios';

// axios.defaults.withCredentials = true
// const TEST_URL_PREFIX = 'http://nftsea.natapp1.cc/api/test';
const TEST_URL_PREFIX = 'http://127.0.0.1:5000/api/test';

export function fetchHello(param, callback) {
    const url = `${TEST_URL_PREFIX}/hello/`;
    axios.post(url, param)
        .then(response => {
            callback(response.data)
        }, errResponse => {
            console.log(errResponse)
        })
}

export function postImg(param, callback) {
    const url = `${TEST_URL_PREFIX}/getImg/`
    axios.post(url, param)
        .then(response => {
            callback(response.data);
        }, errResponse => {
            console.log(errResponse)
        })
}

export function postImgSeg(param, callback) {
    const url = `${TEST_URL_PREFIX}/getImgSeg/`
    axios.post(url, param)
        .then(response => {
            callback(response.data);
        }, errResponse => {
            console.log(errResponse)
        })
}

export function postImgSegNeg(param, callback) {
    const url = `${TEST_URL_PREFIX}/getImgSegNeg/`
    axios.post(url, param)
        .then(response => {
            callback(response.data);
        }, errResponse => {
            console.log(errResponse)
        })
}

export function postSamClear(param, callback) {
    const url = `${TEST_URL_PREFIX}/getSamClear/`
    axios.post(url, param)
        .then(response => {
            callback(response.data);
        }, errResponse => {
            console.log(errResponse)
        })
}

export function postSamClearNew(param, callback) {
    const url = `${TEST_URL_PREFIX}/getSamClearNew/`
    axios.post(url, param)
        .then(response => {
            callback(response.data);
        }, errResponse => {
            console.log(errResponse)
        })
}

export function postText(param, callback) {
    const url = `${TEST_URL_PREFIX}/getText/`
    axios.post(url, param)
        .then(response => {
            callback(response.data);
        }, errResponse => {
            console.log(errResponse)
        })
}


export function postGenerate(param, callback) {
    const url = `${TEST_URL_PREFIX}/postGenerate/`
    axios.post(url, param)
        .then(response => {
            callback(response.data);
        }, errResponse => {
            console.log(errResponse)
        })
}

export function postInstruct(param, callback) {
    const url = `${TEST_URL_PREFIX}/getInstruct/`
    axios.post(url, param)
        .then(response => {
            callback(response.data);
        }, errResponse => {
            console.log(errResponse)
        })
}

export function postInsRetr(param, callback) {
    const url = `${TEST_URL_PREFIX}/getInstructSeg/`
    axios.post(url, param)
        .then(response => {
            callback(response.data);
        }, errResponse => {
            console.log(errResponse)
        })
}

export function postSam(param, callback) {
    const url = `${TEST_URL_PREFIX}/getSam/`
    axios.post(url, param)
        .then(response => {
            callback(response.data);
        }, errResponse => {
            console.log(errResponse)
        })
}

export function postSamNew(param, callback) {
    const url = `${TEST_URL_PREFIX}/getSamNew/`
    axios.post(url, param)
        .then(response => {
            callback(response.data);
        }, errResponse => {
            console.log(errResponse)
        })
}

export function postCompose(param, callback) {
    const url = `${TEST_URL_PREFIX}/getCompose/`
    axios.post(url, param)
        .then(response => {
            callback(response.data);
        }, errResponse => {
            console.log(errResponse)
        })
}

export function reviseText(param, callback) {
    const url = `${TEST_URL_PREFIX}/reviseText/`
    axios.post(url, param)
        .then(response => {
            callback(response.data);
        }, errResponse => {
            console.log(errResponse)
        })
}

export function fetchValue(param, callback) {
    const url = `${TEST_URL_PREFIX}/getValue/`
    axios.get(url, param)
        .then(response => {
            callback(response.data);
        }, errResponse => {
            console.log(errResponse)
        })
}

export function postPrompt(param, callback) {
    const url = `${TEST_URL_PREFIX}/getPrompt/`
    axios.post(url, param)
        .then(response => {
            callback(response.data);
        }, errResponse => {
            console.log(errResponse)
        })
}

export function fetchPrompt(param, callback) {
    const url = `${TEST_URL_PREFIX}/fetchPrompt/`
    axios.post(url, param)
        .then(response => {
            callback(response.data);
        }, errResponse => {
            console.log(errResponse)
        })
}

export function postAxis(param, callback) {
    const url = `${TEST_URL_PREFIX}/postAxis/`
    axios.post(url, param)
        .then(response => {
            callback(response.data);
        }, errResponse => {
            console.log(errResponse)
        })
}

export function addGenerate(param, callback) {
    const url = `${TEST_URL_PREFIX}/addGenerate/`
    axios.post(url, param)
        .then(response => {
            callback(response.data);
        }, errResponse => {
            console.log(errResponse)
        })
}

export function postContext(param, callback) {
    const url = `${TEST_URL_PREFIX}/postContext/`
    axios.post(url, param)
        .then(response => {
            callback(response.data);
        }, errResponse => {
            console.log(errResponse)
        })
}

export function postPath(param, callback) {
    const url = `${TEST_URL_PREFIX}/postPath/`
    axios.post(url, param)
        .then(response => {
            callback(response.data);
        }, errResponse => {
            console.log(errResponse)
        })
}

export function postLAMP(param, callback) {
    const url = `${TEST_URL_PREFIX}/postLAMP/`
    axios.post(url, param)
        .then(response => {
            callback(response.data);
        }, errResponse => {
            console.log(errResponse)
        })
}

export function postBLIP(param, callback) {
    const url = `${TEST_URL_PREFIX}/postBLIP/`
    axios.post(url, param)
        .then(response => {
            callback(response.data);
        }, errResponse => {
            console.log(errResponse)
        })
}
    export function inputCaption(param, callback) {
        const url = `${TEST_URL_PREFIX}/inputCaption/`
        axios.post(url, param)
            .then(response => {
                callback(response.data);
            }, errResponse => {
                console.log(errResponse)
            })
}

export function postLayout(param, callback) {
    const url = `${TEST_URL_PREFIX}/getLayout/`
    axios.post(url, param)
        .then(response => {
            callback(response.data);
        }, errResponse => {
            console.log(errResponse)
        })
}



