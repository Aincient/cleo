import React from "react";



const NumberContext = React.createContext(); //passing initial value

class FacetProvider extends React.Component {
  state = {
    activeFacets: 'test'
  }
  facetHandler = (name, raw) => {

    this.setState({activeFacets: name})
  }

  render() {
    return(
      <NumberContext.Provider value={this.state.activeFacets}>
        
          {this.props.children}
      </NumberContext.Provider>
    )
  }
}


export default FacetProvider;