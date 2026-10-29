import {useState} from "react";
import {Routes,Route,Link,Navigate,useNavigate,useLocation} from "react-router-dom";
import "./App.css";
const products=[
  {id:1, name:"Headphones",price:1500},
  {id:2, name:"Smart Watch",price:3000},
  {id:3, name:"Shoes",price:1200},
  {id:4,name:"Mobile Phone", price:10000}
];

const money=(amount)=> new Intl.NumberFormat("en-IN",{
  style:"currency",
  currency:"INR",
  maximumFractionDigits:0,
}).format(amount);

function App(){

  const [search,setSearch]=useState("");
  const [cart,setCart]=useState([]);
  const [loggedIn,setLoggedIn]=useState(localStorage.getItem("loggedIn")=="true");
  const total=cart.reduce((sum , item)=>sum+item.price*item.quantity,0);
  const totalItems=cart.reduce((sum,item)=>sum+item.quantity,0);
  // const addToCart=(product)=>{setCart((previous)=>{const existing=previous.find((item)=> item.id==product.id);
  //   if(existing)
  //   {
  //     return previous.map((item)=> item.id===product.id ? {...item,quantity:item.quantity+1}:item);
  //   }
  //   return [...previous, {...product,quantity:1}];
  // });
  const addToCart = (product) => {
  setCart((previous) => {
    const existing = previous.find(
      (item) => item.id === product.id
    );

    if (existing) {
      return previous.map((item) =>
        item.id === product.id
          ? { ...item, quantity: item.quantity + 1 }
          : item
      );
    }

    return [...previous, { ...product, quantity: 1 }];
  });
};   // <-- Missing

  const changeQuantity=(id,amount)=>{
    setCart((previous)=>previous.map((item)=>item.id===id ? {...item,quantity:item.quantity+amount}:item)
  .filter((item)=>item.quantity > 0));
  };
  const removeItem=(id)=>{
    setCart((previous)=>previous.filter((item)=>item.id!=id));
  };
  const logout=()=>{
    localStorage.removeItem("loggedIn");
    setLoggedIn(false);
  };
  return (
    <>
    <header className="navbar">
      <Link to="/" className="logo"> Amazon Practice</Link>
      <input className="search" type="search" placeholder="Search for products..." value={search} onChange={(e)=>setSearch(e.target.value)}/>

      <nav>
        <Link to="/">Home</Link>
        <Link to="/cart">Cart({totalItems})</Link>

        {loggedIn ?(<button onClick={logout}>Logout</button>):(<Link to="/login">Login</Link>)}
      </nav>
    </header>

    <main className="container">
      <Routes>
        <Route path="/" element={<Home search={search} addToCart={addToCart}/>}/>
        <Route path="/cart" element={<Cart cart={cart} total={total} loggedIn={loggedIn} changeQuantity={changeQuantity} removeItem={removeItem}/>}/>
        <Route path="/login" element={<Login loggedIn={loggedIn} setLoggedIn={setLoggedIn}/>}/>
        <Route path="/payment" element={loggedIn?(<Payment cart={cart} total={total} setCart={setCart}/>) :(<Navigate to="/login?redirect=/payment" replace />)}/>
        <Route path="/success" element={<Success/>}/>
        <Route path="*" element={<NotFound/>}/>
      </Routes>
    </main>
    <footer>Amazon Prctice Project | React Only Demo Payment</footer>
    </>
  );
}

function Home({search,addToCart}){
  const filteredProducts=products.filter((product)=> product.name.toLowerCase().includes(search.toLowerCase()));

  return (
    <>
    <section className="hero">
      <h1> Welcome to Amazon Practice</h1>
      <p>Search products and start shopping!</p>
    </section>
    <h2>Products</h2>
    <div className="products">
      {filteredProducts.map((product)=>(
        <article className="card" key={product.id}>
          <h3>{product.name}</h3>
          <p className="price">{money(product.price)}</p>
          <button onClick={()=> addToCart(product)}>Add to cart</button>
        </article>
      ))}
    </div>
    {filteredProducts.length===0 && (<p>No products found.</p>)}
    </>
  );
}

function Cart({
    cart,
    total,
    loggedIn,
    changeQuantity,
    removeItem
  }){
    const navigate=useNavigate();

    const proceedToPayment=()=>{
      if(cart.length===0){
        alert("Your cart is empty!");
      return;
    }
    if (loggedIn){
      navigate("/payment");
    }
    else{
      navigate("/login?redirect=/payment");
    }
  };

  return (
    <>
    <h1>Your shopping cart</h1>
    {cart.length===0 ? (
      <section className="panel">
        <p>Your cart is emply.</p>
        <Link className="button-link" to="/">Continue Shopping</Link>
      </section>
    ):(
      <>
      {cart.map((item)=>(
        <article className="cart-item" key={item.id}>
          <div className="cart-details">
            <h3>{item.name}</h3>
            <p>{money(item.price)} each</p>

            <div className ="quantity">
              <button onClick={()=>changeQuantity(item.id,-1)}>
                -
              </button>
              <span>{item.quantity}</span>

              <button onClick={()=>changeQuantity(item.id,1)}>+</button>
              </div> 
              <button className="remove" onClick={()=>removeItem(item.id)}>Remove</button>
          </div>
          <strong>
            {money(item.price*item.quantity)}
          </strong>
        </article>
      ))}
      <section className="panel checkout">
        <h2>Total: {money(total)}</h2>
        <button onClick={proceedToPayment}>Proceed to Payment</button>
      </section>
    </>
    )}
    </>
  );
}


function Login({loggedIn,setLoggedIn}) {
  const navigate=useNavigate();
  const location=useLocation();

  const redirect=new URLSearchParams(location.search).get("redirect") || "/";

  if(loggedIn){
    return <Navigate to={redirect} replace />;
  }
  const handleLogin=(e)=>{
    e.preventDefault();

    localStorage.setItem("loggedIn","true");
    setLoggedIn(true);

    navigate(redirect,{replace:true});
  };
  return (
    <section className="form-card">
      <h1>Login</h1>
      <p>Login to Continue shopping.</p>

      <form onSubmit={handleLogin}>
        <label>Email</label>
        <input type="email" placeholder="Enter email" required />
        <label>Password</label>
        <input type="password" placeholder="Enter password" required />
        <button type="submit">Login</button>
      </form>

      <p className="hint">Demo only: any valid email and non empty password work.</p>
    </section>
  );
}

function Payment({cart,total,setCart})
{
  const navigate=useNavigate();
  const[number,setNumber]=useState("");
  const handlePayment=(e)=>{
    e.preventDefault();

  if(cart.length===0){
    alert("Your cart is empty!");
    navigate("/");
    return;
  }

  if(!/^\d+$/.test(number.trim())){
    alert("Please enter digits only");
    return;
  }
  const order={
    orderNumber:Math.floor(100000+Math.random()*9000),
    amount:total,
    date:new Date().toLocaleString(),
  };

  sessionStorage.setItem(
    "lastOrder",JSON.stringify(order)
  );
  setCart([]);
  navigate("/success");
};

  return(
    <section className="form-card">
    <h1>Payment Page</h1>
    <h2>Total:{money(total)}</h2>

    <p> Enter any number to simulate payment</p>
    <form onSubmit={handlePayment}>
      <label>Payment Number</label>
      <input type="text" inputMode="numeric" placeholder="For example: 1234567890" value={number} onChange={(e)=>setNumber(e.target.value)} required />
      <button type="submit">Pay Now</button>
    </form>

    <p className="hint">This is a demo. No real payment is processed</p>
    </section>
  );
}

function Success(){
  const order=JSON.parse(
    sessionStorage.getItem("lastOrder") || "null"
  );
  return (
    <section className="success-card">
      <h1>order Placed successfully!</h1>
      <p>Thank you for shopping with us.</p>

      {order && (
        <>
        <p>Order Number: #{order.orderNumber}</p>
        <p>Order Amount: {money(order.amount)}</p>
        <p className="hint">{order.date}</p>
        </>
      )}

      <Link className="button-link" to="/">Continue shopping</Link>
    </section>
  );
}

function NotFound(){
  return(
    <section className="success-card">
      <h1>404-Page Not Found</h1>
      <p>The page you are requested does not exists.</p>
      <Link className="button-link" to="/">
      Go to home page</Link>
    </section>
  );
}

export default App;