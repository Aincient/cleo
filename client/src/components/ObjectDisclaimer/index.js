import React, { Component } from 'react'

import translations from '../../shared/translations';

import * as S from './objectdisclaimer.module.css';

const links = {
  rmo_nl: {
    image: 'http://creativecommons.org/licenses/by/3.0/nl/',
    text: 'http://creativecommons.org/about/cc0',
    info: 'http://www.rmo.nl/collectie/open-data',
    imageText: 'CC BY 3.0 NL',
    textText: 'CC0',

  },
  brooklynmuseum_org: {
    image: 'https://creativecommons.org/licenses/by/3.0/',
    text: 'https://creativecommons.org/licenses/by/3.0/',
    info: 'https://www.brooklynmuseum.org/copyright',
    imageText: 'CC BY 3.0',
    textText: 'CC BY 3.0',
  },
  thewalters_org: {
    image: 'https://creativecommons.org/publicdomain/zero/1.0/',
    text: 'https://www.gnu.org/copyleft/fdl.html',
    info: 'https://art.thewalters.org/license/',
    imageText: 'CC0 1.0',
    textText: 'GNU Free Documentation License',
  },
  metmuseum_org: {
    image: 'https://creativecommons.org/publicdomain/zero/1.0/',
    text: 'https://creativecommons.org/publicdomain/zero/1.0/',
    info: 'https://www.metmuseum.org/about-the-met/policies-and-documents/image-resources',
    imageText: 'CC0 1.0',
    textText: 'CC0 1.0',
  },

}

class ObjectDisclaimer extends Component {
  
  render () {
    const {lang, collection} = this.props;
    return (
      <div className={S.root}>
        <div>
          <span className={S.info}>
            {translations(lang).disclaimer['lang_disclaimer']}
          </span>
        </div>
        <div>
          <span className={S.info}>
            {translations(lang).disclaimer['image_rights']}
          </span>
        </div>
        <div>
          <span>
            <a
              className={S.link}
              target="_blank"
              rel="noopener noreferrer" 
              href={links[collection].image}>
              {translations(lang).disclaimer['image']}: {links[collection].imageText}
            </a>
          </span>
          <span>
            <a
              className={S.link}
              target="_blank"
              rel="noopener noreferrer"
              href={links[collection].text}>
              {translations(lang).disclaimer['text']}: {links[collection].textText}
            </a>
          </span>
          <span>
            <a
              className={S.link}
              target="_blank"
              rel="noopener noreferrer" 
              href={links[collection].info}>
              {translations(lang).disclaimer['info']}
            </a>
          </span>
        </div>
      </div>
    )
  }
}

export default ObjectDisclaimer