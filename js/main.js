const imageButton = document.getElementById("image-button");
const imageResult = document.getElementById("image-result");

imageButton.style.display = "none";
imageResult.style.display = "none";
imageResult.innerHTML = "";

let latestRecommendation = "";
const bodyTypeMap = {
    wave: "웨이브형",
    straight: "스트레이트형",
    natural: "내추럴형",
    unknown: "잘 모르겠음"
};

const personalColorMap = {
    "spring-warm": "봄 웜톤",
    "summer-cool": "여름 쿨톤",
    "autumn-warm": "가을 웜톤",
    "winter-cool": "겨울 쿨톤",
    unknown: "잘 모르겠음"
};

const occasionMap = {
    school: "학교",
    work: "출근",
    date: "데이트",
    friends: "친구 약속",
    formal: "격식 있는 자리",
    musical: "공연 / 뮤지컬",
    travel: "여행",
    "casual-outing": "편한 외출"
};

const styleMoodMap = {
    neat: "단정한",
    casual: "캐주얼한",
    feminine: "여성스러운",
    lovely: "러블리한",
    chic: "시크한",
    minimal: "미니멀한"
};

const preferenceMap = {
    waist: "허리선 강조",
    "lower-body": "하체 커버",
    "upper-body": "상체 커버",
    "long-legs": "다리가 길어 보이게",
    comfortable: "편안한 핏"
};
const cityCoordinates = {
    seoul: {
        name: "서울",
        latitude: 37.5665,
        longitude: 126.9780
    },

    incheon: {
        name: "인천",
        latitude: 37.4563,
        longitude: 126.7052
    },

    busan: {
        name: "부산",
        latitude: 35.1796,
        longitude: 129.0756
    },

    daegu: {
        name: "대구",
        latitude: 35.8714,
        longitude: 128.6014
    },

    daejeon: {
        name: "대전",
        latitude: 36.3504,
        longitude: 127.3845
    },

    gwangju: {
        name: "광주",
        latitude: 35.1595,
        longitude: 126.8526
    },

    jeju: {
        name: "제주",
        latitude: 33.4996,
        longitude: 126.5312
    }
};
let currentWeatherData = null;
const weatherButton = document.getElementById("weather-button");
weatherButton.addEventListener("click", async function () {

    const selectedCity = document.getElementById("city").value;

    if (selectedCity === "") {
        alert("지역을 선택해주세요.");
        return;
    }
const city = cityCoordinates[selectedCity];

const weatherResult = document.getElementById("weather-result");

weatherResult.style.display = "block";
weatherResult.innerHTML = "<p>날씨 정보를 불러오는 중입니다...</p>";


const url =
    `https://api.open-meteo.com/v1/forecast` +
    `?latitude=${city.latitude}` +
    `&longitude=${city.longitude}` +
    `&current=temperature_2m,apparent_temperature` +
    `&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max` +
    `&timezone=Asia%2FSeoul`;
try {

    const response = await fetch(url);

    if (!response.ok) {
        throw new Error("날씨 API 요청 실패");
    }

    const data = await response.json();

    const currentTemperature =
        data.current.temperature_2m;

    const apparentTemperature =
        data.current.apparent_temperature;

    const maxTemperature =
        data.daily.temperature_2m_max[0];

    const minTemperature =
        data.daily.temperature_2m_min[0];

    const precipitationProbability =
        data.daily.precipitation_probability_max[0];

        currentWeatherData = {
    city: city.name,
    currentTemperature: currentTemperature,
    apparentTemperature: apparentTemperature,
    maxTemperature: maxTemperature,
    minTemperature: minTemperature,
    precipitationProbability: precipitationProbability
};
    weatherResult.innerHTML = `
        <h3>${city.name}</h3>

        <p>
            <strong>현재 기온:</strong>
            ${currentTemperature}°C
        </p>

        <p>
            <strong>체감 온도:</strong>
            ${apparentTemperature}°C
        </p>

        <p>
            <strong>오늘 최고:</strong>
            ${maxTemperature}°C
        </p>

        <p>
            <strong>오늘 최저:</strong>
            ${minTemperature}°C
        </p>

        <p>
            <strong>강수 확률:</strong>
            ${precipitationProbability}%
        </p>
    `;

} catch (error) {

    weatherResult.innerHTML = `
        <p>
            날씨 정보를 불러오지 못했습니다.
            잠시 후 다시 시도해주세요.
        </p>
    `;

    console.error(error);
}

});
const recommendButton = document.getElementById("recommend-button");

recommendButton.addEventListener("click", async function () {

    const bodyType = document.getElementById("body-type").value;
    const personalColor = document.getElementById("personal-color").value;
    const height = document.getElementById("height").value;

    const occasion = document.getElementById("occasion").value;
    const styleMood = document.getElementById("style-mood").value;
    const extraRequest = document.getElementById("extra-request").value;

    const checkedPreferences = document.querySelectorAll(
        ".checkbox-group input:checked"
    );

    const preferences = [];

    checkedPreferences.forEach(function (checkbox) {
        preferences.push(checkbox.value);
    });
    if (
    bodyType === "" ||
    personalColor === "" ||
    height === "" ||
    occasion === "" ||
    styleMood === ""
    ) {
    alert("필수 정보를 모두 입력해주세요.");
    return;
    }
    if (currentWeatherData === null) {
    alert("먼저 오늘의 날씨를 불러와주세요.");
    return;
    }
    latestRecommendation = "";
    const resultBox = document.getElementById("result");

resultBox.style.display = "block";

resultBox.innerHTML = `
    <p>코디 정보를 분석하는 중입니다...</p>
`;


const koreanPreferences = preferences.map(function (preference) {
    return preferenceMap[preference] || preference;
});


const requestData = {

    weather: currentWeatherData,

    user: {
        bodyType: bodyTypeMap[bodyType] || bodyType,
        personalColor: personalColorMap[personalColor] || personalColor,
        height: height,
        preferences: koreanPreferences
    },

    outfit: {
        occasion: occasionMap[occasion] || occasion,
        styleMood: styleMoodMap[styleMood] || styleMood,
        extraRequest: extraRequest
    }
};


try {

    const response = await fetch("/api/outfit", {

    method: "POST",

    headers: {
        "Content-Type": "application/json"
    },

    body: JSON.stringify(requestData)
});


    if (!response.ok) {
        throw new Error("서버 요청에 실패했습니다.");
    }


    const data = await response.json();

    latestRecommendation = data.recommendation;

    imageButton.style.display = "block";
    resultBox.innerHTML = `
    <h3>오늘의 AI 코디</h3>

    <p>
        ${data.message}
    </p>

    <div class="ai-recommendation">
        ${data.recommendation.replace(/\n/g, "<br>")}
    </div>
`;


} catch (error) {

    resultBox.innerHTML = `
        <p>
            코디 추천을 불러오는 중 오류가 발생했습니다.<br>
            잠시 후 다시 시도해주세요.
        </p>
    `;

    console.error(error);
}
});
imageButton.addEventListener("click", async function () {

    if (!latestRecommendation) {
        alert("먼저 코디 추천을 받아주세요.");
        return;
    }

    const imageResult = document.getElementById("image-result");

    imageResult.style.display = "block";
    imageResult.innerHTML = `
        <p>AI가 코디 이미지를 생성하고 있어요...</p>
    `;

    try {

        const response = await fetch("/api/outfit-image", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        recommendation: latestRecommendation
    })
    });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.error || data.message || "이미지 생성 실패"
            );
        }

        imageResult.innerHTML = `
            <h3>코디 이미지</h3>
            <p>${data.message}</p>
            <img
                src="data:image/png;base64,${data.imageBase64}"
                alt="AI 코디 이미지"
            >
        `;

    } catch (error) {

    imageResult.innerHTML = `
        <p>
            이미지 생성 중 오류가 발생했습니다.<br>
            잠시 후 다시 시도해주세요.
        </p>
    `;

    console.error(error);
}
});
