import React from "react";
import "./App.css";
import * as PIXI from 'pixi.js';
//import './top-view-map.js'; // Import the top-view-map.js file



class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      msgs: [],
      isLoading: true
    };

    this.appRef = React.createRef();

    //this.app = null;
    //
    //document.body.appendChild(this.app.view);


  }

  componentDidMount() {
    this.app = new PIXI.Application({
      width: 1000,
      height: 900,
      backgroundColor: 0x282c34,
      transparent: true
    });

    this.carsNums = new PIXI.Text('', { fontFamily: 'Arial', fontSize: 24, fill: 0xff1010, align: 'center' });
    this.app.stage.addChild(this.carsNums);

    this.cars = new PIXI.Graphics();
    this.app.stage.addChild(this.cars);

    this.track = new PIXI.Graphics();
    this.app.stage.addChild(this.track);
    this.fetchData();

    this.interval = setInterval(() => {
      this.fetchData();
    }, 500); // Fetch data every 0.5 seconds

    let lastTrack = null; // save the last track, draw track only if it changed
    this.interval = setInterval(() => {
      
      fetch("/api/track")
      .then((res) => res.json())
      .then((data) => { 
      console.log(data['track']);
      
      if (data['track'] !== lastTrack) {
        this.track.clear();
        for(var id in data['track']) {
          var value = data['track'][id];
          let a = value[0]; 
          let b = value[1]; 
          let flag = value[2];
          // draw black thick line
          this.track.lineStyle(14, 0xffffff);
          this.track.moveTo(a[0], a[1]); 
          this.track.lineTo(b[0], b[1]);
          if (flag === 0) {
            // if no flag, draw white line
            this.track.lineStyle(10, 0x000000);
            this.track.moveTo(a[0], a[1]); 
            this.track.lineTo(b[0], b[1]);
          } else if (flag === 1) {
            // if flag is blue

            // blue thin line:
            this.track.lineStyle(10, 0x0000ff);
            this.track.moveTo(a[0], a[1]); 
            this.track.lineTo(b[0], b[1]);
          } else if (flag === 2) {
            // if flag is yellow
            // yellow thin line:
            this.track.lineStyle(10, 0xffff00);
            this.track.moveTo(a[0], a[1]); 
            this.track.lineTo(b[0], b[1]);
          }
        }
      }

      lastTrack = data['track'];
      
      //document.body.appendChild(this.app.view);
      this.forceUpdate();
      });

      fetch("/api/competitors")
      .then((res) => res.json())
      .then((data) => { 
      console.log(data['competitors']);

      this.cars.clear();
      for(var key in data['competitors']) {
        var value = data['competitors'][key];
        let x = value[0]; 
        let y = value[1]; 

        this.cars.lineStyle(12, 0xff0000);
        this.cars.drawCircle(x, y, 10);

        this.carsNums.text = key;
        this.carsNums.x = x;
        this.carsNums.y = y;

        
        console.log(key, x, y, value)

      
      }
      });
    }, 25);
    this.appRef.current.appendChild(this.app.view);

  }

  componentWillUnmount() {
    clearInterval(this.interval);
  }

  fetchData = () => {
    fetch("/api/msgs")
      .then((res) => res.json())
      .then((data) => this.setState({ msgs: data['message'], isLoading: false }));
  }

  render() {
    const { msgs, isLoading } = this.state;

    return (
      <div className="App">
        <header className="App-header">
          {isLoading ? (
            <p>Loading...</p>
          ) : (
            <ul>
              {msgs.map((message, index) => (
                <p key={index}>{message}</p>
              ))}
            </ul>
          )}
        </header>
        <div ref={this.appRef}></div>

      </div>
      

    );
    
  }
}

export default App;
