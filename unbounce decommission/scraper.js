const puppeteer = require('puppeteer');

(async() => {
    const browser = await puppeteer.launch({ headless: false, timeout: 60000, args: ['--no-sandbox', '--disable-setuid-sandbox'] })

    pages = await browser.pages();
    page = pages[0];

    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3419.0 Safari/537.36');
    await page.setViewport({ width: 1890, height: 1000 });

    await page.goto('https://app.unbounce.com/430372/pages?show_only=published&direction=desc&sort_option=created_at')

    await page.waitForSelector('input#js_auth_email');

    await page.type('input#js_auth_email', 'office@howtomanageasmalllawfirm.com');
    await page.type('input#js_auth_password', 'PASSWORD');
    await page.click('#login_btn');

    await page.waitForNavigation();

    await page.waitForSelector('li.comp_page-list-item');

    let page_urls = [];
    // page 1    
    //page_urls = page_urls.concat(await page.$$eval('li.comp_page-list-item > a', urls => { return urls.map(url => url.querySelector('h3').textContent.trim() + ':' + url.querySelector('p').textContent.trim()) }))
    page_urls = page_urls.concat(await page.$$eval('li.comp_page-list-item > a', urls => { return urls.map(url => url.querySelector('p').textContent.trim()) }))
        // page forward 
    await page.click('a.js-pjax-pagination[data-page="2"]');
    await page.waitForNavigation();
    await page.waitForSelector('li.comp_page-list-item');
    //page_urls = page_urls.concat(await page.$$eval('li.comp_page-list-item > a', urls => { return urls.map(url => url.querySelector('h3').textContent.trim() + ':' + url.querySelector('p').textContent.trim()) }))
    page_urls = page_urls.concat(await page.$$eval('li.comp_page-list-item > a', urls => { return urls.map(url => url.querySelector('p').textContent.trim()) }))
        // page forward 
    await page.click('a.js-pjax-pagination[data-page="3"]');
    await page.waitForNavigation();
    await page.waitForSelector('li.comp_page-list-item');
    //page_urls = page_urls.concat(await page.$$eval('li.comp_page-list-item > a', urls => { return urls.map(url => url.querySelector('h3').textContent.trim() + ':' + url.querySelector('p').textContent.trim()) }))
    page_urls = page_urls.concat(await page.$$eval('li.comp_page-list-item > a', urls => { return urls.map(url => url.querySelector('p').textContent.trim()) }))
        // page forward 
    await page.click('a.js-pjax-pagination[data-page="4"]');
    await page.waitForNavigation();
    await page.waitForSelector('li.comp_page-list-item');
    //page_urls = page_urls.concat(await page.$$eval('li.comp_page-list-item > a', urls => { return urls.map(url => url.querySelector('h3').textContent.trim() + ':' + url.querySelector('p').textContent.trim()) }))
    page_urls = page_urls.concat(await page.$$eval('li.comp_page-list-item > a', urls => { return urls.map(url => url.querySelector('p').textContent.trim()) }))
        // page forward 
    await page.click('a.js-pjax-pagination[data-page="5"]');
    await page.waitForNavigation();
    await page.waitForSelector('li.comp_page-list-item');
    //page_urls = page_urls.concat(await page.$$eval('li.comp_page-list-item > a', urls => { return urls.map(url => url.querySelector('h3').textContent.trim() + ':' + url.querySelector('p').textContent.trim()) }))
    page_urls = page_urls.concat(await page.$$eval('li.comp_page-list-item > a', urls => { return urls.map(url => url.querySelector('p').textContent.trim()) }))

    console.log(page_urls)

    await browser.close()
})()