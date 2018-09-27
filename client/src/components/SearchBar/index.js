import React, { Component } from 'react'
import classNames from 'classnames';
import {connect} from 'react-redux';

import * as S from './searchbar.module.css';

import Navigation from '../../components/Navigation';
import {UserOptions} from '../../components/UserOptions';

class SearchBar extends Component {
  constructor(props) {
    super(props);
    this.state = {
      query: '',
      lang: 'en'
    }
  }

  componentDidMount = () => {
    const {user} = this.props;
    if(user.account_settings) {
      this.setState({lang: user.account_settings.language})
    }
  }
  

  handleSubmit = (e) => {
    e.preventDefault();
    const {query} = this.state;
    const {handleNewSearch} = this.props;
    handleNewSearch(query);
  }

  handleChange = (e) => {
    this.setState({query: e.target.value})
  }

  render () {
    return (
      <div className={classNames(S.root, 'row')}>
        <div className="col-2 col-md-3">
          <Navigation />
        </div>
        <div className={classNames(S.inputWrapper, 'col-12 col-md-5 order-2 order-md-1')}>
          <form className="col-12 " onSubmit={this.handleSubmit}>
            <div className={classNames(S.inputGroup, 'input-group')}>
              <input type="text" onChange={this.handleChange} />
              <button className={S.submit} type="submit"></button>
            </div>
          </form>
        </div>
        <div className="col-10 order-1 col-md-4 order-md-2">
          <UserOptions />
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

const connectedSearchBar = connect(mapStateToProps)(SearchBar);
export {connectedSearchBar as SearchBar};