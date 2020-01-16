'use strict';

const counter = document.getElementById('counter');
let count = 200001;
const timer = setInterval(() => counter.innerText = (count++ + ' sec'), 1000);

if (module.hot) {
    module.hot.dispose(() => {
        clearInterval(timer);
    });
    module.hot.accept();
}
