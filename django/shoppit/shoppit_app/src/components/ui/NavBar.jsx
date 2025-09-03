import NavLink from './NavLink';
import { FaCartShopping } from 'react-icons/fa6';
import styles from './NavBar.module.css';
import { Link } from 'react-router-dom';

const NavBar = () => {
  return (
    <nav className={`navbar navbar-expand-lg navbar-light bg-white shadow-sm py-3 ${styles.stickyNavbar}`}>
      <div className="container">
        <Link className="navbar-brand fw-bold text-uppercase" to="/">SHOPPITO</Link>
        
        <button 
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarContent"
          aria-controls="navbarContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>

        <div className="collapse navbar-collapse" id="navbarContent">
          <NavLink />
          <Link to="/cart" className={`btn btn-dark ms-1 rounded-pill position-relative ${styles.responsiveCart}`}>
            <FaCartShopping />
            <span 
              className="position-absolute top-0 start-100 translate-middle badge rounded-pill"
              style={{ fontSize: "0.65em", padding: "0.35em 0.65em", backgroundColor: "#dc650b" }}
            >
              0
            </span>
          </Link>
        </div>
      </div>
    </nav>
  );
}

export default NavBar;