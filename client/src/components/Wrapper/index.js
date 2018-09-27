import React from 'react';
import classNames from 'classnames';

import * as S from './wrapper.module.css';

const Wrapper = (props) => {
  let {hasBG} = props;
  return(
    <div className={classNames(S.root, {[S.hasBG]: hasBG})}>      
      {props.children}
      {hasBG && <Copyright text="Travelling Boat being Rowed, The Metropolitan Museum of Art, 20.3.1" />}
      {props.lang &&
        <a
        className={classNames(S.feedback, 'button hide-xs')}
        target="_blank"
        rel="noopener noreferrer" 
        href={`/pages/${props.lang}/feedback/`}>
          Feedback
        </a>
      }
      
    </div>
  )
}

export default Wrapper;


const Copyright = (props) => {
  return (
      <i className={S.copy}>
      i
        <span>{props.text}</span>
      </i>
  )
}