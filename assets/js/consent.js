/* Off The Wall Digital, analytics consent. Loaded in the head of every page by the
   consent block (partials/consent.html), straight after the inline snippet that sets every
   Google consent signal to denied.

   Google Analytics 4 runs in "basic" consent mode: gtag.js is not requested at all until the
   visitor accepts, now or in an earlier visit. With no choice, or a rejection, nothing is
   loaded from googletagmanager.com or google-analytics.com.

   The choice is kept in localStorage under STORE_KEY as "granted" or "denied". Any element
   with data-cookie-settings (the "Cookie settings" footer link) reopens the banner.

   Pages report a lead with window.otwdConsent.lead('form_name'). It only sends when consent
   is granted, and returns true if it did. */

/* ================================================================
   DRAFT wording, awaiting Colin's sign-off.
   Every word the banner shows lives here. UK English, no dashes.
   ================================================================ */
var OTWD_CONSENT_WORDING = {
  title: 'Can I count your visit?',
  body: 'I would like to use Google Analytics cookies to see which pages people read. Nothing is loaded unless you accept, and you can change your mind at any time.',
  privacyLink: 'Read the privacy notice',
  accept: 'Accept',
  reject: 'Reject'
};

(function(){
  var MEASUREMENT_ID = 'G-TJ3F734GY9';
  var STORE_KEY = 'otwd_analytics_consent';
  var PRIVACY_HREF = '/privacy#privacy';
  var W = OTWD_CONSENT_WORDING;

  var loaded = false;
  var banner = null;
  var opener = null;

  function readChoice(){
    try { return window.localStorage.getItem(STORE_KEY); } catch (e) { return null; }
  }
  function saveChoice(v){
    try { window.localStorage.setItem(STORE_KEY, v); } catch (e) {}
  }
  function granted(){ return readChoice() === 'granted'; }

  function startAnalytics(){
    window['ga-disable-' + MEASUREMENT_ID] = false;
    gtag('consent', 'update', { analytics_storage: 'granted' });
    if (loaded) return;
    loaded = true;
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + MEASUREMENT_ID;
    document.head.appendChild(s);
    gtag('js', new Date());
    gtag('config', MEASUREMENT_ID);
  }

  /* Remove _ga and _ga_* on this host and every parent domain (GA sets them on the
     top level domain, e.g. .offthewalldigital.com). */
  function clearGaCookies(){
    var names = document.cookie.split(';').map(function(c){ return c.split('=')[0].trim(); })
      .filter(function(n){ return n === '_ga' || n.indexOf('_ga_') === 0; });
    var parts = location.hostname.split('.');
    var domains = [''];
    for (var i = 0; i < parts.length - 1; i++){ domains.push('; domain=' + parts.slice(i).join('.')); }
    names.forEach(function(n){
      domains.forEach(function(d){
        document.cookie = n + '=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/' + d;
      });
    });
  }

  function stopAnalytics(){
    gtag('consent', 'update', { analytics_storage: 'denied' });
    /* If gtag.js already loaded on this page, stop it sending anything more. */
    window['ga-disable-' + MEASUREMENT_ID] = true;
    clearGaCookies();
  }

  function choose(v){
    var before = readChoice();
    saveChoice(v);
    if (v === 'granted') startAnalytics();
    else if (before === 'granted' || loaded) stopAnalytics();
    closeBanner();
  }

  function el(tag, attrs, text){
    var n = document.createElement(tag);
    for (var k in attrs){ n.setAttribute(k, attrs[k]); }
    if (text) n.textContent = text;
    return n;
  }

  function buildBanner(){
    banner = el('section', { 'class': 'cc', 'aria-labelledby': 'ccTitle', hidden: '' });
    banner.appendChild(el('h2', { 'class': 'cc__title', id: 'ccTitle', tabindex: '-1' }, W.title));
    var p = el('p', { 'class': 'cc__body' }, W.body + ' ');
    p.appendChild(el('a', { href: PRIVACY_HREF }, W.privacyLink));
    banner.appendChild(p);
    var row = el('div', { 'class': 'cc__actions' });
    var acc = el('button', { type: 'button', 'class': 'cc__btn', 'data-consent': 'granted' }, W.accept);
    var rej = el('button', { type: 'button', 'class': 'cc__btn', 'data-consent': 'denied' }, W.reject);
    row.appendChild(acc);
    row.appendChild(rej);
    banner.appendChild(row);
    acc.addEventListener('click', function(){ choose('granted'); });
    rej.addEventListener('click', function(){ choose('denied'); });
    document.body.appendChild(banner);
  }

  function openBanner(focus){
    if (!banner) buildBanner();
    banner.hidden = false;
    if (focus) banner.querySelector('.cc__title').focus();
  }

  function closeBanner(){
    if (!banner) return;
    var hadFocus = banner.contains(document.activeElement);
    banner.hidden = true;
    if (hadFocus && opener && document.contains(opener)) opener.focus();
    opener = null;
  }

  if (granted()) startAnalytics();

  function ready(){
    var links = document.querySelectorAll('[data-cookie-settings]');
    for (var i = 0; i < links.length; i++){
      links[i].addEventListener('click', function(e){
        e.preventDefault();
        opener = this;
        openBanner(true);
      });
    }
    var c = readChoice();
    if (c !== 'granted' && c !== 'denied') openBanner(false);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', ready);
  else ready();

  window.otwdConsent = {
    lead: function(formName){
      if (!granted() || !loaded) return false;
      gtag('event', 'generate_lead', { form_name: formName });
      return true;
    }
  };
})();
