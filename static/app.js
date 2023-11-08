const BASE_URL = "http://localhost:5000/api";
const cupcakesUl = $("ul");
$(document).ready(function () {
  showCupcakes();
});

function generateCupcakeHtml(cupcake) {
  return `<li data-cupcake-id=${cupcake.id}>${cupcake.flavor}
    </li>`;
}

async function showCupcakes() {
  const response = await axios.get(`${BASE_URL}/cupcakes`);
  const cupcakes = response.data.cupcakes;
  cupcakes.forEach((cupcake) => {
    let cupcakeLi = generateCupcakeHtml(cupcake);
    cupcakesUl.append(cupcakeLi);
  });
}

$("#cupcakeForm").on("submit", async function (event) {
  event.preventDefault();

  const flavor = $("#flavor").val();
  const size = $("#size").val();
  const rating = $("#rating").val();
  const image = $("#image").val();

  const data = {
    flavor: flavor,
    size: size,
    rating: rating,
    image: image,
  };
  const response = await axios.post(`${BASE_URL}/cupcakes`, data);
  let newCupcake = response.data.cupcake;
  let newLi = generateCupcakeHtml(newCupcake);
  cupcakesUl.append(newLi);
  $("#cupcakeForm input").val("");
});
