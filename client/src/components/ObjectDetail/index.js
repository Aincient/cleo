import React, { Component } from 'react'
import constants from '../../shared/constants';
import classNames from 'classnames';
import {
  withScriptjs,
  withGoogleMap,
  GoogleMap,
  Marker,
} from "react-google-maps";
import {Link, withRouter} from 'react-router-dom';
import {connect} from 'react-redux';
import { Carousel } from 'react-responsive-carousel';

import {savedObjectsActions} from '../../actions/savedObjects.actions';

import * as FileDownload from '../../shared/multiDownload';

import translations from '../../shared/translations';
import noImage from '../../images/noimage.png'; 
import ObjectDisclaimer from '../ObjectDisclaimer';

import dataSvc from '../../api';

import {getPrevObj, getNextObj} from '../../helpers';

import * as S from './objectdetail.module.css';

class ObjectDetail extends Component {

  constructor(props) {
    super(props);

    this.state = {
      hasSimilarImages: false,
      isLoading: false,
      similarObjects: [],
      classified: [],
      lang: 'en',
      fromResults: true,
      object: {},
      objectInCollection: false,
      fav_id: null,
      isDropdownOpen: false
    }
  }

  componentDidMount = () => {
    const {user} = this.props;
    window.scrollTo(0, 0);
    if(user.account_settings) {
      this.setState({lang: user.account_settings.language})
    }
    document.addEventListener('mousedown', this.handleClickOutside);
  }

  componentWillMount = () => {
    document.removeEventListener('mousedown', this.handleClickOutside);
  }

  handleClickOutside = (event) => {
    
  }

  setWrapperRef = (node) => {
    this.wrapperRef = node;
  }

  componentDidUpdate = () => {
    const {savedObjects, object} = this.props;
    const {objectInCollection} = this.state;
    if(savedObjects.objects) {
      let isObjectInCollection = savedObjects.objects.some(obj => obj.collection_item === object.id);
      if(isObjectInCollection) {
        if(!objectInCollection) {
          let objInCollection = savedObjects.objects.filter(obj => obj.collection_item === object.id);
          this.setState({
            objectInCollection: true,
            fav_id: objInCollection[0].id
          })
        }
      } 
    }
  }

  handleObjectSave = (id) => {
    const {dispatch} = this.props;
    if(id) {
      dispatch(savedObjectsActions.add(id))
    }
  }

  handleObjectRemove = (id) => {
    const {dispatch} = this.props;
    if(id) {
      dispatch(savedObjectsActions.remove(id))
      this.setState({
        objectInCollection: false,
        fav_id: null
      })
    }
  }

  getSimilarObjects = (id) => {
    if(id) {
      this.setState({isLoading: true});
      dataSvc.searchCollectionAI(id)
        .then(obj=> {
          this.setState({
            isLoading: false,
            hasSimilarImages: true,
            similarObjects: obj.data.results
          })
        })
    }
  }

  toggleDownloadMenu = () => {
    this.setState({isDropdownOpen: !this.state.isDropdownOpen});
  }

  handleImageDownload = (e) => {
    e.preventDefault();
    const {object} = this.props;
    if(object) {
      object.images_urls.map(img => {
        FileDownload(constants.api.url +img.lr , `${object.id}.jpg`);
      })
    }
  }

  goBack = () => {
    this.props.goBack();
  }


  render () {
    const {
      hasSimilarImages, 
      similarObjects, 
      objectInCollection, 
      fav_id,
      isLoading,
      isDropdownOpen
    } = this.state;
    const {
      objects, 
      object, 
      handleObjectDetail,
    } = this.props;
    let prevItem, nextItem;
    let backToHome = false;
    let showMap = true;
    if(objects.length > 0) {
      let prevItemId = getPrevObj(object.id, objects);
      let nextItemId = getNextObj(object.id, objects);
      if(prevItemId >= 0) {
        if(objects[prevItemId]) {
          if(objects[prevItemId].images.length > 0) {
            prevItem = (<div className={S.prevItem} onClick={()=> handleObjectDetail(objects[prevItemId])}> <span><img src={constants.api.url + objects[prevItemId].images_urls[0].th}  alt="" /></span></div>)
          } else {
            prevItem = (<div className={S.prevItem} onClick={()=> handleObjectDetail(objects[prevItemId])}> <span><img style={{maxHeight: 120}} src={noImage}  alt="" /></span></div>)
          }
        }
      }
      if(nextItemId >= 0) {
        if(objects[nextItemId]) {
          if(objects[nextItemId].images.length > 0) {
            nextItem = (<div className={S.nextItem} onClick={()=> handleObjectDetail(objects[nextItemId])}> <span><img src={constants.api.url + objects[nextItemId].images_urls[0].th} alt=""/></span></div>)
          } else {
            nextItem = (<div className={S.nextItem} onClick={()=> handleObjectDetail(objects[nextItemId])}> <span><img style={{maxHeight: 120}} src={noImage} alt=""/></span></div>)
          }
        }
      }
    } else {
      backToHome = true;
    }
    const {lang} = this.state;
    if(object.location) {
      if(object.location.lat === "-90.0" || object.location.long === "-180.0") {
        showMap = false;
      }
    }

  
    return (
      <div className={S.root}>
        <div className={S.header}>
        {
            backToHome ? (
              <Link to="/search/" className={S.goBack}>{`<`} {translations(lang)['goToHome']}</Link>
            ) : (
              <span className={S.goBack} onClick={() => this.goBack()}> {`<`} {translations(lang)['backToResults']}</span>
            )
          }

         
        </div>
        <div className="row">
          <div className="col col-lg-7">
            <div className="row">
            <div className="col-12 col-md">
              <div className={classNames(S.relatedFromSerie, "row")}>
                {prevItem && (
                  <div className="col">
                  {prevItem}
                  </div>
                )}
                <div className="col">
                  
                </div>
                {nextItem && (
                  <div className="col">
                    {nextItem}
                  </div>
                )}
                
              </div>
              <div className={S.image}>
                  {object.images ? (
                    <div className="row">
                    <Carousel showThumbs={false} dynamicHeight={true} className={S.carousel}>
                      {object.images_urls.map((img, i) => {
                        return(
                          <div key={i}>
                            <img src={constants.api.url + img.lr} alt=""/>
                          </div>
                        )
                      })}
                    </Carousel>
                    </div>
                  ): (<img src={noImage} alt=""/>) 
                  }
              </div>
              <div className={classNames(S.buttonContainer, "row")}>
                <div className="col">
                    <button
                      onClick={(e)=> this.handleImageDownload(e)}
                      className={classNames(S.downloadObject, 'button-secondary')}>
                        {translations(lang)['download_images']}
                    </button> 
                    <div 
                      ref={this.setWrapperRef}
                      className={classNames("dropdown", {['active']: isDropdownOpen})}
                      onClick={() => this.toggleDownloadMenu()}>
                      <button type="button" className={classNames(S.downloadObject, 'dropdown-trigger button button-secondary')}>Download Object</button>
                      <div className={classNames("dropdown-menu", S.dropdownMenu)}>
                        <a
                          href={`/api/collectionitem/${object.id}/download/?docformat=xlsx`}
                          download="object">
                            {translations(lang)['download_ojbect']} (Excel)
                        </a>
                        <a
                          href={`/api/collectionitem/${object.id}/download/`}
                          download="object">
                            {translations(lang)['download_ojbect']} (CSV)
                        </a>
                      </div>
                    </div>
                    {objectInCollection ? (
                      <button
                        className={classNames(S.removeObject,'button-danger' )}
                        onClick={() => this.handleObjectRemove(fav_id)}>
                        {translations(lang)['delete_object']}
                      </button> 
                    ): (
                      <button
                      className={classNames(S.saveObject )}
                      onClick={() => this.handleObjectSave(object.id)}>
                        {translations(lang)['save_object']}
                      </button> 
                    )}
                   
                </div>
              </div>
            </div>
            </div>
            <div className={classNames(S.objectWrapper, 'row')}>
              <div className="col">
                <h3 className={S.objectTitle}>
                  {lang === 'en' ? (object.title_en.length === 1 ? object.title_en : object.title_en.map(title=> `${title}; `) ) : (object.title_nl.length === 1 ? object.title_nl : object.title_nl.map(title=> `${title}; `))}
                </h3>
                {
                  object.importer_uid !== 'metmuseum_org' ? (
                    lang === 'en' ? object.description_en && <Item title="Description" items={object.description_en} /> : object.description_nl && <Item title="Beschrijving" items={object.description_nl} />
                  ) : (null)
                }
                {object.dimensions && <Item title={lang === 'en' ? 'Dimensions' : 'Dimensies' } items={object.dimensions} />}
                { lang === 'en' ?  object.country_en && <Item title="Country" items={object.country_en} /> :  object.country_nl && <Item title="Land" items={object.country_nl} />}
                { lang === 'en' ?  object.city_en && <Item title="City" items={object.city_en} /> :  object.city_nl && <Item title="Stad" items={object.city_nl} />}
                { lang === 'en' ?  object.region_en && <Item title="Region" items={object.region_en} /> :  object.region_nl && <Item title="Regio" items={object.region_nl} />}
                { lang === 'en' ?  object.sub_region_en && <Item title="Sub region" items={object.sub_region_en} /> :  object.sub_region_nl && <Item title="Sub regio" items={object.sub_region_nl} />}
                { lang === 'en' ?  object.locale_en && <Item title="Locale" items={object.locale_en} /> :  object.locale_nl && <Item title="Locale" items={object.locale_nl} />}
                {
                  object.importer_uid === 'metmuseum_org'  ? (
                       lang === 'en' ? object.description_en && <Item title="Locus" items={object.description_en} /> : object.description_nl && <Item title="Locus" items={object.description_nl} />
                  ) : (null)
                }
                
                { lang === 'en' ?  object.excavation_en && <Item title="Excavation" items={object.excavation_en} /> :  object.excavation_nl && <Item title="Opgraving" items={object.excavation_nl} />}
                
                { lang === 'en' ?  object.provenance_en && <Item title="History" items={object.provenance_en} /> :  object.provenance_nl && <Item title="Geschiedenis" items={object.provenance_nl} />}

                {
                  object.importer_uid !== 'rmo_nl' ? (
                    lang === 'en' ? object.acquired_en && <Item title="Acquired" items={object.acquired_en} /> : object.acquired_nl && <Item title="Verworven" items={object.acquired_nl} />
                  ) : (null)
                }
                
                
                { lang === 'en' ?  object.credit_line_en && <Item title="Credit line" items={object.credit_line_en} /> :  object.credit_line_nl && <Item title="Credit line" items={object.credit_line_nl} />}
                { lang === 'en' ?  object.museum_collection_en && <Item title="Department" items={object.museum_collection_en} /> :  object.museum_collection_en && <Item title="Afdeling" items={object.museum_collection_en} />}
                { lang === 'en' ?  object.style_en && <Item title="Style" items={object.style_en} /> :  object.style_en && <Item title="Stijl" items={object.style_en} />}
                { lang === 'en' ?  object.culture_en && <Item title="Culture" items={object.culture_en} /> :  object.culture_en && <Item title="Cultuur" items={object.culture_en} />}
                { lang === 'en' ?  object.inscriptions_en && <Item title="Inscriptions" items={object.inscriptions_en} /> :  object.inscriptions_en && <Item title="Inscripties" items={object.inscriptions_en} />}

                { lang === 'en' ?  object.keywords_en && <Item title="Keywords" items={object.keywords_en} /> :  object.keywords_nl && <Item title="Trefwoorden" items={object.keywords_nl} />}
                { lang === 'en' ?  object.references_en && <Item title="References" items={object.references_en} /> :  object.references_en && <Item title="Referenties" items={object.references_en} />}
                {lang === 'en' ? object.department_en && <Item title='Department' items={object.department_en} /> :  object.department_nl && <Item title="Afdeling" items={object.department_nl} />}
                {lang === 'en' ? object.material_detail_en && <Item title="Material" items={object.material_detail_en} /> :  object.material_detail_nl && <Item title="Materiaal" items={object.material_detail_nl} /> }
                {lang === 'en' ? object.object_type_detail_en && <Item title="Object type" items={object.object_type_detail_en} /> : object.object_type_detail_nl && <Item title="Object type" items={object.object_type_detail_nl} /> }
                {lang === 'en' ? object.inventory_number && <Item title="Inventory number" items={object.inventory_number} /> : object.inventory_number &&  <Item title="Inventarisnummer" items={object.inventory_number} />}
                
                { lang === 'en' ? object.period_en && <Item title="Period" items={object.period_en} /> : object.period_nl && <Item title="Periode" items={object.period_nl} />}
                { lang === 'en' ? object.dynasty_en && <Item title="Dynasty" items={object.dynasty_en} /> :  object.dynasty_nl && <Item title="Dynastie" items={object.dynasty_nl} />}
                { lang === 'en' ? object.reign_en && <Item title="Reign" items={object.reign_en} /> :  object.reign_nl && <Item title="Regering" items={object.reign_nl} />}
                
                
                

                
                
                
                {object.importer_uid && (
                  <div className="row">
                    <div className={classNames(S.title, "col-12 col-md-4 col-lg-3")}>{translations(lang).facets['importer_uid']}</div>
                    <div className="col-12 col-md-8 col-lg-9">
                      <a
                      target="_blank"
                      rel="noopener noreferrer"
                      href={object.api_url}>{translations(lang).collections[object.importer_uid]}</a>
                    </div>
                  </div>
                )}
              </div>
              <div className={S.langdisclaimer}>
                <ObjectDisclaimer lang={lang} collection={object.importer_uid} />
              </div>
            </div>
          </div>
          <div className="col-12 col-lg-5">
              {showMap && <MapWithAMarker
                googleMapURL="https://maps.googleapis.com/maps/api/js?key=AIzaSyAf_eQq5uTTxMSQ1dFYsmtpTgaaOwbQ0_c&v=3&libraries=geometry,drawing,places"
                loadingElement={<div style={{ height: `100%` }} />}
                containerElement={<div style={{ height: `500px`, overflow: 'hidden', marginBottom: '20px' }} />}
                mapElement={<div style={{ height: `100%` }} />} 
                location={object.location}
                />
              }
              
              <SimilarImages 
                hasSimilarImages={hasSimilarImages}
                lang={lang} 
                isLoading={isLoading}
                object={object.id}
                getSimilarObjects={this.getSimilarObjects}
                handleObjectDetail={handleObjectDetail}
                results={similarObjects} />
           
          </div>
        </div>
      </div>
    )
  }
}

const mapStateToProps = (state, ownProps) => {
  const { authentication: {user}, savedObjects } = state;
  return {
      savedObjects,
      user
  };
}

const connectedObjectDetail = withRouter(connect(mapStateToProps)(ObjectDetail));
export {connectedObjectDetail as ObjectDetail};

const Item = (props) => {
  let items = props.items;
  let comp = null;

  if(items !== '_') {
    if(!Array.isArray(items)) {
      items = [items];
    }
    comp = (
      <div className={classNames(S.objectDetailRow, "row", {[S.period]: props.title === 'Period' || props.title === 'Periode' })}>
      <div className={classNames(S.title, "col-12 col-md-4 col-lg-3")}>{props.title}</div>
      <div className="col-12 col-md-8 col-lg-9">
        {
         items.map((res, index) => <span key={index} className={S.tag}>{res}</span>)
        }
      </div>
    </div>
    )
   
  }
  
  
  return (
    comp
  )
}

const MapWithAMarker = withScriptjs(withGoogleMap(props =>
  <GoogleMap
    defaultZoom={6}
    defaultCenter={{lat: parseFloat(props.location.lat), lng: parseFloat(props.location.lon)}}>
      <Marker position={{lat: parseFloat(props.location.lat), lng: parseFloat(props.location.lon)}} />
  </GoogleMap>
));


const SimilarImages = (props) => {
  return (
    <div className={classNames(S.similarImages)}>
      {props.hasSimilarImages ? (
        <div className={S.imageWrapper}>
        {props.results ?
          props.results.map((object, i)=> {
            return(
            <div 
              key={i}
              onClick={() => props.handleObjectDetail(object)}
              className={S.similarImage}
              style={{backgroundImage: "url(" + constants.api.url + object.images_urls[0].lr + ")"}}>
            </div>
            )
            }) : (<div>{translations(props.lang)['no_results']}</div>)
        }
          
          </div>
      ) : (
        props.isLoading ? (
          <span className="loader loader-dark"></span>
        ) : (
        <button 
          onClick={()=> props.getSimilarObjects(props.object)}>
          {translations(props.lang)['show_similar_images']}
        </button>
        )
      )}
    </div>
    
  )
}

const ObjetsInCollection = (props) => {
  return(
    <div className="row">
      {props.objects.map((obj, index)=> {
        return(
         <div key={index} onClick={()=> props.handleObjectDetail(obj)}>
           {obj.images_urls && <img src={obj.images_urls[0]}   alt="image"/>  }
         </div>
        )
      })}
    </div>
  )
}