import React, { Component } from 'react'
import {connect} from 'react-redux';
import {
  withScriptjs,
  withGoogleMap,
  GoogleMap,
  Marker,
  InfoWindow
} from "react-google-maps";

import constants from '../../shared/constants';

import translations from '../../shared/translations';
import { MarkerClusterer } from "react-google-maps/lib/components/addons/MarkerClusterer";

import * as S from './map.module.css';

class Map extends Component {

  constructor (props) {
    super(props)
    this.state = {
      lang: 'en',
      openWindows: []
    }
  }

  componentDidMount = () => {
    const {user} = this.props;
    if(user.account_settings) {
      this.setState({lang: user.account_settings.language})
    }  
  }

  goToRoute = (object) => {
    this.props.handleObjectDetail(object);
  }

  handleToggle = (window) => {
    const {openWindows} = this.state;
    if(window) {
      if(openWindows.includes(window)) {
        let filteredArray = this.state.openWindows.filter(item => item !== window)
        this.setState({openWindows: filteredArray});
      } else {
        this.setState({
          openWindows: [...this.state.openWindows, window]
        })
      }
    }
  }

  isWindowOpen = (window) => {
    const {openWindows} = this.state;
    if(openWindows.includes(window)) {
      return true;
    }
  }

  render () {
    const {objects} = this.props;
    const {lang} = this.state;
    return (
      <div className={S.root}>
        <span className={S.info}>{translations(lang)['mapInfo']}</span>
        <div className={S.wrapper}>
          <MapWithAMarker
              googleMapURL="https://maps.googleapis.com/maps/api/js?key=AIzaSyAf_eQq5uTTxMSQ1dFYsmtpTgaaOwbQ0_c&v=3&libraries=geometry,drawing,places"
              loadingElement={<div style={{ height: `100%` }} />}
              containerElement={<div style={{ height: `400px`, overflow: 'hidden' }} />}
              mapElement={<div style={{ height: `100%` }} />} 
              results={objects}
              onToggleOpen={this.handleToggle}
              isWindowOpen={this.isWindowOpen}
              goToRoute={this.goToRoute}
            />
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

const connectedMap = connect(mapStateToProps)(Map);
export {connectedMap as Map};

const MapWithAMarker = withScriptjs(withGoogleMap(props =>
  <GoogleMap
    defaultZoom={5}
    defaultCenter={{ lat: 26.8206, lng: 30.8025 }}>
    <MarkerClusterer
      averageCenter
      enableRetinaIcons
      gridSize={60}>
    {props.results.map(res=> {
      return (
        
        <Marker
        key={res.id}
        position={{lat: parseFloat(res.location.lat), lng: parseFloat(res.location.lon)}} 
        onClick={(e) => props.onToggleOpen(res.id)}>
          {props.isWindowOpen(res.id) && 
           <InfoWindow  onCloseClick={(e) => props.onToggleOpen(res.id)}>
           <div className="row">
            {res.images_urls[0].lr &&
            <div className="col">
               
            <img style={{maxWidth: 120, maxHeight: 120}} src={constants.api.url + res.images_urls[0].lr} alt=""/>
          </div> 
               }
             
             <div className="col">
               <div onClick={() =>props.goToRoute(res)}>
               {res.title_en.map(t=> `${t}; `)}
               </div>
             </div>
            
           </div>
         </InfoWindow>
          }
         
        </Marker>

      )
    })}
    </MarkerClusterer>
  </GoogleMap>
));
