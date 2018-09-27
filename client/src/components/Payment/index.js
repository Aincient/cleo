import React, { Component } from 'react'
import {connect} from 'react-redux';
import dataSvc from '../../api';
import * as S from './payment.module.css';

import classNames from 'classnames';

import translations from '../../shared/translations';

class Payment extends Component {

  constructor(props) {
    super(props);
      this.state = {
        payment: {
          first_name: '',
          last_name: '',
          adress: '',
          city: '',
        },
        submitted: false,
        initLang: 'en',
        product: '',
        isInsideNL: true
      };
    }

  componentDidMount = () => {
    dataSvc.getProdcuts()
    .then((res) => {
      this.setState({
        product: res.data.results[0]
      })
    })
  }

  handleCheckout = (id) => {
    dataSvc.checkoutOrder(id).then((res)=> {
      window.location.href = res.data.redirect
    });
  }

  handleCheckbox = () => {
    this.setState({isInsideNL: !this.state.isInsideNL});
  }

  render () {
    const { product, isInsideNL } = this.state;
    const {accountInfo, lang} = this.props;

    let queries, showPayment;
    if(accountInfo) {
      if(accountInfo.scope === 'super_user' || accountInfo.scope === 'unlimited_access_user' || accountInfo.scope === 'subscribed_group_user') {
        queries = `${translations(lang).userOptions['unlimited']}`;
        showPayment = false;
      } else {
        queries =  `${accountInfo.num_requests_left} ${translations(lang).userOptions['creditsLeft']}`
        showPayment = true
      }
    }   
    return (
      <div className={S.root}>
        <div className="wrapper">
          <div className={S.paymentwrapper}>
            <div className="row">
              <div className="col-12 col-md-6">
                <div className={S.accountWrapper}>
                  <div className={S.account}>
                    <div className={S.type}>
                      Account
                    </div>
                    <div className={S.credits}>
                      {queries}
                    </div>
                  </div>
                </div>
              </div>
              <div className="col-12 col-md-6">
                {showPayment && (
                   <div className={S.buynew}>
                 <div className={S.buyNewTitle}>
                 {translations(lang)['buynewnoticebutton']}
               </div>
               <div className={classNames(S.price)}>
                    {product ? (
                      <Product 
                        {...product} 
                        handleCheckout={this.handleCheckout} 
                        isInsideNL={isInsideNL}
                        lang={lang} />
                          ) : null}
                  </div>
                <div className={classNames(S.checkBoxWrapper, {[S.checked]: isInsideNL})}>
                  <div className={classNames("input-field", S.inutfield)}>
                    <input 
                      checked={isInsideNL || ''}
                      id="insideNL" 
                      onChange={this.handleCheckbox}
                      name="insideNL" 
                      type="checkbox" />
                    <label 
                      
                      htmlFor="insideNL">
                      {translations(lang).userOptions['locationCheck']}
                    </label>
                  </div>
                </div>
                  <div>
                  </div> 
                </div>
                 ) }
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }
}

const mapStateToProps = (state, ownProps) => {
  const { authentication: {user} } = state;
  return {
      user
  };
}

const connectedPayment = connect(mapStateToProps)(Payment);
export {connectedPayment as Payment};


const Product = (props) => {
  return (
    <div className={S.productWrapper}>
      <div className={S.productInfo}>
        <span className={S.productPrice}>€ {Number(props.price).toLocaleString("nl-NL", {minimumFractionDigits: 2})}</span> <span className={S.productCount}>/ {props.num_requests} queries</span> 
        <span className={S.taxes}>{props.lang === 'nl' ? `Inclusief` : `Including`} 21% {props.isInsideNL ? `BTW` : `VAT`}</span>
      </div>
      {props.isInsideNL ? (
        <button onClick={() => props.handleCheckout(props.code)}>{translations(props.lang).userOptions['buynewButton']}</button>
      ): (
        props.lang === 'nl' ? (
          <a 
            href={`mailto:heleen@aincient.org?subject=Ik%20wil%20nieuwe%20queries%20aanvragen&body=Prijs%3A%20€${Number(props.price).toLocaleString("nl-NL", {minimumFractionDigits: 2})}%0AQueries%3A%20${props.num_requests}%0A%0ANaam%0AGebruikersnaam%3A%0APersoonlijk%20%2F%20Zakelijk%3A%20%0ABedrijfsnaam%20(alleen%20zakelijk)%3A%20%0ABTW%20nr%20(alleen%20zakelijk)%3A%0AAdres%3A%20%0ALand%3A`}
           className="button">
           {translations(props.lang).userOptions['contactus']}
         </a>
           ): (
             <a 
             href={`mailto:heleen@aincient.org?subject=I%20would%20like%20to%20buy%20new%20queries&body=Price%3A%20€${Number(props.price).toLocaleString("nl-NL", {minimumFractionDigits: 2})}%0AQueries%3A%20${props.num_requests}%0A%0AName%0AUsername%3A%0APersonal%20%2F%20Business%3A%20%0ACompany%20name%20(if%20business)%3A%20%0AVAT%20Number%20(if%20business)%3A%0AAdres%3A%20%0ACountry%3A`}
               className="button">
               {translations(props.lang).userOptions['contactus']}
             </a>
           )
      )}
    </div>
  )
}